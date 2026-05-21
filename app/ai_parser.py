import re
from datetime import datetime
from typing import Optional


CATEGORY_KEYWORDS = {
    "food": ["mcdonald", "kfc", "indomaret", "alfamart", "grab food", "gofood", "shopeefood",
             "warteg", "resto", "restaurant", "cafe", "kopi", "coffee", "makan", "bakso",
             "burger", "pizza", "sushi", "nasi", "ayam"],
    "transport": ["grab", "gojek", "maxim", "bluebird", "taxi", "ojek", "commuter", "busway",
                  "transjakarta", "toll", "parkir", "bensin", "pertamina", "shell", "spbu"],
    "shopping": ["shopee", "tokopedia", "lazada", "blibli", "tiktok shop", "bukalapak",
                 "zalora", "sociolla", "fashion", "baju", "sepatu", "tas"],
    "health": ["kimia farma", "guardian", "apotek", "apotik", "klinik", "dokter", "rumah sakit",
               "rs ", "puskesmas", "vitamin", "obat"],
    "entertainment": ["netflix", "spotify", "youtube", "steam", "playstore", "appstore",
                      "bioskop", "cgv", "cinepolis", "xxi", "game"],
    "bills": ["pln", "pdam", "telkom", "indihome", "wifi", "internet", "listrik", "air",
              "iuran", "tagihan", "cicilan"],
    "transfer": ["transfer", "kirim uang", "setor", "tarik tunai", "atm"],
}

PAYMENT_KEYWORDS = {
    "GoPay": ["gopay"],
    "OVO": ["ovo"],
    "DANA": ["dana"],
    "ShopeePay": ["shopeepay", "spay"],
    "BCA": ["bca", "klik bca", "myBCA"],
    "Mandiri": ["mandiri", "livin"],
    "BRI": ["bri", "brimo"],
    "BNI": ["bni", "bni mobile"],
    "CIMB": ["cimb", "octo"],
    "Jenius": ["jenius"],
    "Flip": ["flip"],
    "Debit": ["debit", "kartu debit"],
    "Kredit": ["kredit", "credit card", "kartu kredit", "visa", "mastercard"],
    "Tunai": ["tunai", "cash", "uang tunai"],
}


def parse_amount(text: str) -> float:
    """Extract Rupiah amount from text."""
    text_clean = text.replace(".", "").replace(",", ".")
    # Pattern: Rp 150.000 or Rp150000 or IDR 150000
    patterns = [
        r"(?:Rp\.?\s*|IDR\s*)(\d+(?:[.,]\d+)*)",
        r"(\d{4,})(?:\s*(?:rupiah|idr))",
    ]
    for pattern in patterns:
        match = re.search(pattern, text_clean, re.IGNORECASE)
        if match:
            raw = match.group(1).replace(",", "").replace(".", "")
            try:
                return float(raw)
            except ValueError:
                continue
    return 0.0


def detect_category(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return "other"


def detect_payment_method(text: str) -> str:
    text_lower = text.lower()
    for method, keywords in PAYMENT_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return method
    return "Unknown"


def extract_merchant(text: str) -> str:
    """Try to extract merchant name from notification text."""
    # Pattern: "di <Merchant>" or "ke <Merchant>" or "at <Merchant>"
    patterns = [
        r"(?:di|ke|at|from|to)\s+([A-Za-z0-9\s&'.]+?)(?:\s+(?:sebesar|senilai|Rp|IDR|untuk|with)|\.|,|$)",
        r"(?:pembayaran|bayar|payment)\s+(?:ke\s+)?([A-Za-z0-9\s&'.]+?)(?:\s+(?:berhasil|sukses|success|Rp|IDR)|\.|,|$)",
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:menerima|received)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            merchant = match.group(1).strip()
            if 2 < len(merchant) < 50:
                return merchant
    # Fallback: first capitalized word group
    caps = re.findall(r"[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+)*", text)
    if caps:
        return caps[0]
    return "Unknown Merchant"


def extract_date(text: str) -> str:
    """Extract date from text or return today."""
    patterns = [
        r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",
        r"(\d{4})-(\d{2})-(\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            groups = match.groups()
            if len(groups[2]) == 4 and int(groups[2]) > 2000:
                return f"{groups[2]}-{groups[1].zfill(2)}-{groups[0].zfill(2)}"
            elif len(groups[0]) == 4:
                return f"{groups[0]}-{groups[1]}-{groups[2]}"
    return datetime.now().strftime("%Y-%m-%d")


def parse_expense(text: str) -> dict:
    return {
        "amount": parse_amount(text),
        "merchant": extract_merchant(text),
        "category": detect_category(text),
        "payment_method": detect_payment_method(text),
        "date": extract_date(text),
        "raw_text": text,
    }
