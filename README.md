# AutoSpend AI 🤖💸

AI-powered expense logger — parse transaction notifications automatically using regex + keyword intelligence.

## Features

- Parse teks notifikasi transaksi (SMS, email, app notification)
- Ekstrak: nominal Rupiah, merchant, kategori, payment method, tanggal
- Simpan ke SQLite
- REST API via FastAPI
- Swagger UI otomatis di `/docs`

---

## Cara Install

```bash
# Clone repo
git clone https://github.com/rudiuciha/autospend-ai.git
cd autospend-ai

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup env
cp .env.example .env
```

---

## Cara Jalan

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Buka Swagger UI: http://localhost:8000/docs

---

## Contoh curl

### Cek status
```bash
curl http://localhost:8000/
```

### Parse transaksi
```bash
curl -X POST http://localhost:8000/expenses/parse \
  -H "Content-Type: application/json" \
  -d '{"text": "Pembayaran GoPay ke McDonald Sudirman berhasil. Nominal Rp 45.000 pada 22/05/2026."}'
```

**Response:**
```json
{
  "id": 1,
  "amount": 45000.0,
  "merchant": "McDonald Sudirman",
  "category": "food",
  "payment_method": "GoPay",
  "date": "2026-05-22",
  "raw_text": "Pembayaran GoPay ke McDonald Sudirman berhasil...",
  "created_at": "2026-05-22T10:00:00"
}
```

### Lihat semua transaksi
```bash
curl http://localhost:8000/expenses
```

### Lihat summary
```bash
curl http://localhost:8000/expenses/summary
```

**Response:**
```json
{
  "total_expenses": 145000.0,
  "total_transactions": 3,
  "by_category": {
    "food": 45000.0,
    "transport": 100000.0
  },
  "by_payment_method": {
    "GoPay": 145000.0
  }
}
```

---

## Struktur Project

```
autospend-ai/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app & endpoints
│   ├── models.py        # Pydantic models
│   ├── ai_parser.py     # Transaction parser logic
│   └── expense_store.py # SQLite storage
├── docs/
│   └── xiaomi-submission.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** — REST API framework
- **Pydantic** — data validation
- **SQLite** — lightweight local database
- **uvicorn** — ASGI server
