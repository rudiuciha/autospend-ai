from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from .models import ExpenseInput, Expense
from .ai_parser import parse_expense
from .expense_store import init_db, save_expense, get_all_expenses, get_summary
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AutoSpend AI",
    description="AI-powered expense logger — parse transaction notifications automatically.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "AutoSpend AI",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.post("/expenses/parse", response_model=Expense)
def parse_and_save(body: ExpenseInput):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    parsed = parse_expense(body.text)
    if parsed["amount"] == 0.0:
        raise HTTPException(status_code=422, detail="Could not extract amount from text")
    expense = save_expense(parsed)
    return expense


@app.get("/expenses", response_model=List[Expense])
def list_expenses():
    return get_all_expenses()


@app.get("/expenses/summary")
def expenses_summary():
    return get_summary()
