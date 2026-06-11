import config
import os
import re
import time
import random
import config
import logging
import pyperclip
import pandas as pd

from pynput import keyboard
from collections import deque
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# ==================================================
# CONFIG
# ==================================================

STOP_FLAG = config.STOP_FLAG
CHATGPT_URL = config.CHATGPT_URL
PROMPT_TEXTAREA_ID = config.PROMPT_TEXTAREA_ID
VOICE_BUTTON_SELECTOR = config.VOICE_BUTTON_SELECTOR
COPY_BUTTON_SELECTOR = config.COPY_BUTTON_SELECTOR
COMPANY_KNOWLEDGE_SELECTOR = config.COMPANY_KNOWLEDGE_SELECTOR
LIMIT_KEYWORDS = config.LIMIT_KEYWORDS
EXCEL_FILE = config.EXCEL_FILE
EXCEL_SHEET = config.EXCEL_SHEET
PROMPT_BASE = config.PROMPT_BASE
# ==================================================
# LOGGING
# ==================================================


os.makedirs("logs", exist_ok=True)

log_file = (
    "logs/automation_"
    + time.strftime("%Y-%m-%d")
    + ".log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            log_file,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

# ==================================================
# SELENIUM HELPERS
# ==================================================

def find_element(driver, by, selector):
    try:
        return driver.find_element(by, selector)
    except Exception:
        return None


def find_elements(driver, by, selector):
    try:
        return driver.find_elements(by, selector)
    except Exception:
        return []


def find_chatgpt_tab(driver):
    for handle in driver.window_handles:
        driver.switch_to.window(handle)

        if CHATGPT_URL in driver.current_url.lower():
            logging.info(
                f"Tab ditemukan: {driver.current_url}"
            )
            return driver

    return None


def get_prompt(driver):
    return find_element(
        driver,
        By.ID,
        PROMPT_TEXTAREA_ID
    )


def get_voice_button(driver):
    return find_element(
        driver,
        By.CSS_SELECTOR,
        VOICE_BUTTON_SELECTOR
    )


def get_company_knowledge(driver):
    return find_element(
        driver,
        By.CSS_SELECTOR,
        COMPANY_KNOWLEDGE_SELECTOR
    )


def copy_last_response(driver):
    buttons = find_elements(
        driver,
        By.CSS_SELECTOR,
        COPY_BUTTON_SELECTOR
    )

    if not buttons:
        return None

    driver.execute_script(
        "arguments[0].click();",
        buttons[-1]
    )

    time.sleep(1)

    return pyperclip.paste()


# ==================================================
# ACTIONS
# ==================================================

def create_new_chat(driver):
    body = driver.find_element(By.TAG_NAME, "body")

    body.send_keys(
        Keys.CONTROL + Keys.SHIFT + "o"
    )

    time.sleep(3)

    if not get_company_knowledge(driver):
        add_company_knowledge(driver)
        
    send_base_prompt(driver)

    wait_response_finished(driver)

    logging.info("New Chat dibuat")


def refresh_page(driver):
    body = driver.find_element(By.TAG_NAME, "body")

    body.send_keys(
        Keys.CONTROL + "r"
    )

    logging.info("Page di-refresh")

    time.sleep(2)


def add_company_knowledge(driver):

    prompt = get_prompt(driver)

    if not prompt:
        return False

    prompt.send_keys("/company")
    prompt.send_keys(Keys.ENTER)

    time.sleep(2)

    logging.info("Company Knowledge ditambahkan")

    return True

def send_base_prompt(driver):
    prompt = get_prompt(driver)
    pyperclip.copy(PROMPT_BASE)
    prompt.send_keys(Keys.CONTROL + "v")
    time.sleep(1)
    prompt.send_keys(Keys.ENTER)
    logging.info("Base prompt has sent")

def is_base_prompt_has_sent(driver):
    try:
        code_prompt = "CP08062026"
        body = driver.find_element(By.TAG_NAME, "body")
        return code_prompt in body.get_attribute("textContent")
    except Exception:
        return False

def add_window_response_time(window, response_time, maxlen):
    if len(window) == maxlen:
        window.popleft()
    window.append(response_time)
    total_response_time = sum(window)
    avg_response_time = total_response_time / len(window)
    return window, avg_response_time

def wait_by_response(response_text):
    len_text = len(response_text)
    second = len_text // 80
    random_time = random.randint(second, second + 3)
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < random_time and not STOP_FLAG:
        time.sleep(1)
    return True

# ==================================================
# VALIDATION
# ==================================================

def wait_response_finished(
    driver,
    timeout_minutes=2
):
    timeout_seconds = timeout_minutes * 60

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:

        if STOP_FLAG:
            return True
            break

        clear_prompt(driver)

        if get_voice_button(driver):
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.END)
            time.sleep(1)
            return True

        time.sleep(3)

    return False


def is_limit_reached(driver):

    try:

        page_text = (
            driver.find_element(
                By.TAG_NAME,
                "body"
            )
            .text
            .lower()[-1000:]
        )

        return any(
            keyword in page_text
            for keyword in LIMIT_KEYWORDS
        )

    except Exception as e:

        logging.error(
            f"Check limit gagal: {e}"
        )

        return False

def clear_prompt(driver):

    prompt = get_prompt(driver)

    if not prompt:
        return False

    value = prompt.get_attribute("textContent")

    if value:
        prompt.send_keys(
            Keys.CONTROL + "a"
        )
        prompt.send_keys(
            Keys.BACKSPACE
        )

        time.sleep(0.5)

        return True

# ==================================================
# DATA
# ==================================================

def save_result(
    data,
    index,
    code,
    response
):

    original_text = response.replace(
        "\r\n",
        "\n"
    )

    tokens = re.split(
        r"[ ,:/\n()]+|\[.*?\]",
        original_text
    )

    tokens = [x for x in tokens if x]

    if code in tokens:

        data.loc[index, "description"] = (
            original_text
        )

        data.loc[index, "status"] = (
            "Success"
        )

        return True

    data.loc[index, "description"] = (
        "Code Not Found in Text"
    )

    data.loc[index, "status"] = (
        "Failed"
    )

    return False


# ==================================================
# BUSINESS LOGIC
# ==================================================

def process_row(
    driver,
    data,
    index,
    row,
    random_wait=False
):

    company_knowledge = (
        get_company_knowledge(driver)
    )

    # Sementara pada pengujian, company knowledge selalu aktif
    # company_knowledge = True

    if not company_knowledge:

        logging.warning(
            "Company Knowledge belum aktif"
        )

        add_company_knowledge(driver)

        return

    clear_prompt(driver)

    prompt = get_prompt(driver)

    if not prompt:

        logging.warning(
            "Prompt tidak ditemukan"
        )

        refresh_page(driver)

        return

    prompt.send_keys(row["name"])
    prompt.send_keys(Keys.ENTER)

    logging.info(
        f"Processing {row['name']} in idx {index}"
    )

    if not wait_response_finished(driver):

        if is_limit_reached(driver):

            logging.warning(
                "Limit reached"
            )

            create_new_chat(driver)

        else:

            logging.warning(
                "Timeout response (3 minutes)"
            )

            refresh_page(driver)

            if is_base_prompt_has_sent(driver) == False:
                send_base_prompt(driver)

        return

    response = copy_last_response(driver)

    if not response:

        logging.error(
            "Copy response gagal"
        )

        return

    saved = save_result(
        data=data,
        index=index,
        code=row["code"],
        response=response
    )

    if saved:
        logging.info(
            f"Success : {row['code']}"
        )
        return True
    else:
        logging.error(
            f"Code tidak ditemukan : {row['code']}"
        )
        return False

    wait_by_response(response)


# ==================================================
# HOTKEY
# ==================================================

def on_press(key):

    global STOP_FLAG

    try:

        if key.char == "q":

            logging.info(
                "Q ditekan, program berhenti"
            )

            STOP_FLAG = True

    except AttributeError:
        pass


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":
    options = Options()
    options.debugger_address = config.ADDRESS_IP

    driver = webdriver.Chrome(
        options=options
    )

    driver = find_chatgpt_tab(driver)

    if not driver:
        raise Exception(
            "Tab ChatGPT tidak ditemukan"
        )

    if not is_base_prompt_has_sent(driver):
        if not get_company_knowledge(driver):
            add_company_knowledge(driver)
        send_base_prompt(driver)
        wait_response_finished(driver)

    else:
        logging.info(
            "Base prompt has already sent"
        )

    data = pd.read_excel(
        EXCEL_FILE,
        sheet_name=EXCEL_SHEET,
        dtype=str
    )

    listener = keyboard.Listener(
        on_press=on_press
    )

    listener.start()

    minlen = config.MIN_SAMPLES
    maxlen = config.MAX_LEN
    window = deque(maxlen=maxlen)
    total_response_time = 0

    try:

        save_counter = 0

        for index, row in data.iterrows():

            if STOP_FLAG:
                break

            if "success" in str(row["status"]).lower() or pd.notna(row["status"]):
                continue

            start_time = time.perf_counter()

            process_row(
                driver,
                data,
                index,
                row,
                random_wait=True
                )

            end_time = time.perf_counter()

            response_time = end_time - start_time

            window, avg_response_time = add_window_response_time(
                window,
                response_time,
                maxlen
            )

            if len(window) >= minlen and avg_response_time > config.AVG_RESPONSE_TIME_LIMIT:
                create_new_chat(driver)

                logging.info(
                    f"Avg response time > {config.AVG_RESPONSE_TIME_LIMIT} seconds, create new chat"
                )

            if len(window) >= minlen and avg_response_time < config.AVG_RESPONSE_TIME_LIMIT_BOTTOM:
                if is_limit_reached(driver):
                    STOP_FLAG = True
                    logging.info(
                        f"Avg response time < {config.AVG_RESPONSE_TIME_LIMIT_BOTTOM} seconds and limit reached"
                    )
                    break

            save_counter += 1

            if save_counter % 5 == 0:

                data.to_excel(
                    EXCEL_FILE,
                    index=False,
                    sheet_name=EXCEL_SHEET
                )

                logging.info(
                    "Auto save"
                )

    finally:

        data.to_excel(
            EXCEL_FILE,
            index=False,
            sheet_name=EXCEL_SHEET
        )

        listener.stop()

        logging.info(
            "Program selesai"
        )