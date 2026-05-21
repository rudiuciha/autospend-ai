# AutoSpend AI — Xiaomi MiMo Submission

## Ide

**AutoSpend AI** adalah expense logger berbasis AI yang bisa mem-parse teks notifikasi transaksi secara otomatis — tanpa perlu input manual.

---

## Problem

Pengguna smartphone di Indonesia menerima puluhan notifikasi transaksi per hari (GoPay, OVO, DANA, BCA, dll). Tidak ada cara mudah untuk:
- Melacak pengeluaran secara otomatis
- Mengkategorikan transaksi tanpa input manual
- Mendapat insight pengeluaran harian/mingguan

---

## Solusi

AutoSpend AI membaca teks notifikasi dan mengekstrak:
- **Nominal** — Rp 45.000
- **Merchant** — McDonald Sudirman
- **Kategori** — food, transport, shopping, health, dll
- **Payment method** — GoPay, OVO, BCA, dll
- **Tanggal** — dari teks atau fallback ke hari ini

Semua tersimpan otomatis ke database lokal.

---

## Potensi Integrasi MiMo

Dengan kemampuan reasoning **Xiaomi MiMo**, AutoSpend AI bisa:

1. **Smart Categorization** — MiMo menentukan kategori dengan konteks lebih dalam (bukan hanya keyword matching)
2. **Anomaly Detection** — "Pengeluaran kamu naik 40% minggu ini di kategori food"
3. **Natural Language Query** — "Berapa total aku belanja di Shopee bulan ini?"
4. **Budget Recommendation** — Saran anggaran berdasarkan pola spending
5. **Multi-language Parsing** — Notifikasi dalam berbagai bahasa/format

---

## Tech Stack

- FastAPI (Python)
- SQLite
- Regex + keyword NLP parser
- Ready untuk integrasi LLM API (MiMo)

---

## Target User

- Pengguna aktif e-wallet Indonesia (GoPay, OVO, DANA)
- Mobile-first, tidak perlu input manual
- Privacy-first: data tersimpan lokal

---

## Roadmap

| Phase | Feature |
|---|---|
| MVP | Parse + store via API |
| v1 | Telegram bot integration |
| v2 | MiMo AI reasoning layer |
| v3 | Dashboard + export CSV |

---

*Submitted by: rudiuciha — AutoSpend AI MVP*
