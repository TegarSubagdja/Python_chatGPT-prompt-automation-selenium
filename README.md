# Instalasi library
### Buat venv
```bash
python -m venv venv
```
### Aktifkan venv
```bash
venv\Scripts\activate.bat
```
### Instalasi library
```bash
pip install --no-index --find-links=./packages -r requirements.txt
```
# Clone chrome profile
```bash
xcopy "C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data\Profile 1" "C:\ChromeSelenium\User Data\Profile 1" /E /H /C /I /Y
```
# Open Chrome
```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeAutomation\User Data" --profile-directory="Profile 1"
```
atau cara otomatis
```bash
python appOpenChrome.py
```
# Run app
```bash
python app.py
```
