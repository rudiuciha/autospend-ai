from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExpenseInput(BaseModel):
    text: str


class Expense(BaseModel):
    id: Optional[int] = None
    amount: float
    merchant: str
    category: str
    payment_method: str
    date: str
    raw_text: str
    created_at: Optional[str] = None
