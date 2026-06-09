ADDRESS_IP = "127.0.0.1:9222"

MAX_LEN = 10

AVG_RESPONSE_TIME_LIMIT = 60

STOP_FLAG = False

CHATGPT_URL = "chatgpt.com"

PROMPT_TEXTAREA_ID = "prompt-textarea"

VOICE_BUTTON_SELECTOR = (
    'button[aria-label="Start Voice"]'
)

COPY_BUTTON_SELECTOR = (
    'button[aria-label="Copy response"]'
)

COMPANY_KNOWLEDGE_SELECTOR = (
    'button[aria-label="Company knowledge, click to remove"]'
)

LIMIT_KEYWORDS = [
    "reach the maximum",
    "you've reached the maximum",
    "starting a new chat",
]

EXCEL_FILE = "Data/data.xlsx"
EXCEL_SHEET = "Sheet1"

PROMPT_BASE = """
Tugas CP08062026:

Tarik data dari company knowledge berdasarkan kode produk yang akan saya berikan.

Aturan keluaran WAJIB:

1. Keluaran harus berupa plain text murni.
2. Jangan gunakan markdown apa pun.
3. Jangan gunakan code block.
4. Jangan gunakan format bash.
5. Jangan gunakan tabel.
6. Jangan gunakan emoji, ikon, simbol dekoratif, atau karakter khusus.
7. Hasil harus siap copy-paste langsung ke Excel atau CSV.
8. Gunakan format dan urutan field persis seperti contoh.
9. Jangan menambahkan field baru di luar format yang ditentukan.
10. Jika suatu informasi tidak ditemukan pada company knowledge, isi dengan:
    Tidak ditemukan
11. Jika kode produk tidak ditemukan sama sekali, tetap tampilkan seluruh format dan jelaskan pada bagian catatan bahwa data produk tidak ditemukan di company knowledge.
12. Jangan menambahkan penjelasan, disclaimer, atau kalimat pembuka maupun penutup.

Format keluaran:

[NAMA PRODUK]

Deskripsi marketplace:

[deskripsi produk dalam format marketplace]

Data teknis:
Brand: [nilai]
Kode produk: [nilai]
Kategori: [nilai]
Seri: [nilai]
Rasio gear: [nilai]
Tipe gearhead: [nilai]
Kompatibilitas referensi: [nilai]
Aplikasi: [nilai]
Fungsi: [nilai]

catatan:
[keterangan tambahan atau "Tidak ada"]

Contoh:

ORIENTAL 2GN50K

Deskripsi marketplace:

Gearhead Oriental Motor 2GN50K merupakan parallel shaft gearhead seri 2GN dengan rasio reduksi 50:1 untuk motor Oriental Motor tipe GN pinion shaft. Produk ini digunakan untuk aplikasi yang membutuhkan penurunan kecepatan lebih besar dan peningkatan torsi output, seperti conveyor kecil, feeder, rotary mechanism, packaging machine, indexing sederhana, dan kebutuhan replacement gearhead Oriental Motor.

Data teknis:
Brand: Oriental Motor
Kode produk: 2GN50K
Kategori: Parallel shaft gearhead / reducer
Seri: 2GN / GN-K gearhead
Rasio gear: 50:1
Tipe gearhead: Parallel Shaft GN-K Gearhead
Kompatibilitas referensi: motor Oriental Motor 2IK6GN / 2RK6GN pinion shaft type
Aplikasi: mesin industri ringan, otomasi, conveyor kecil, feeder, rotary mechanism, equipment produksi
Fungsi: menurunkan speed dan meningkatkan torsi output

catatan:
Tidak ada

"""