import json

text = """ORIENTAL 2GN50K

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

params = [
    "Deskripsi marketplace:",
    "Data teknis:",
    "Brand:",
    "Kode produk:",
    "Kategori:",
    "Seri:",
    "Rasio gear:",
    "Tipe gearhead:",
    "Kompatibilitas referensi:",
    "Aplikasi:",
    "Fungsi:",
    "catatan:"
]

def extract_section(text: str, start_marker: str, end_marker: str | None = None) -> str:
    text_lower = text.lower()

    start = text_lower.find(start_marker.lower())
    if start == -1:
        return ""

    start += len(start_marker)

    if end_marker:
        end = text_lower.find(end_marker.lower(), start)
        if end == -1:
            end = len(text)
    else:
        end = len(text)

    return text[start:end].strip()

def parse_product(text: str, params: list[str]) -> dict:
    result = {}

    for start, end in zip(params, params[1:]):
        key = start.replace(":", "").strip()

        value = extract_section(text, start, end)

        result[key] = value

    return result

parsed = parse_product(text, params)

print(json.dumps(parsed, indent=4, ensure_ascii=False, sort_keys=True))