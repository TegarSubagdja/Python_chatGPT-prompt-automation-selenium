import random

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
Tidak ada"""

print(f"Panjang asli : {len(text)}")

panjang_text = len(text.split())/80

batas_bawah = int(panjang_text)
batas_atas = int(panjang_text + 3)

print(f"Batas bawah adalah {batas_bawah}")
print(f"Batas atas adalah {batas_atas}")
print(random.randint(batas_bawah, batas_atas))