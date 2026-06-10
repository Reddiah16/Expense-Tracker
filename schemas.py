from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal


# --- USER SCHEMAS ---

class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    # Password intentionally excluded from all responses

    class Config:
        from_attributes = True


# --- AUTH SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str


# --- EXPENSE SCHEMAS ---

class ExpenseCreate(BaseModel):
    title: str
    amount: Decimal
    category: str
    date: date  # expects "YYYY-MM-DD" format


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: Decimal
    category: str
    date: date

    class Config:
        from_attributes = True


# Summary schema for dashboard totals
class CategorySummary(BaseModel):
    category: str
    total: Decimal
