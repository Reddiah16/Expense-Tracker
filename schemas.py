from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date
from decimal import Decimal


class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True


# --- USER SCHEMAS ---

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(BaseOrmModel):
    id: int
    email: str
    # Password intentionally excluded from all responses


# --- AUTH SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str


# --- EXPENSE SCHEMAS ---

class ExpenseCreate(BaseModel):
    title: constr(min_length=1)
    amount: Decimal
    category: constr(min_length=1)
    date: date  # expects "YYYY-MM-DD" format


class ExpenseUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    amount: Optional[Decimal] = None
    category: Optional[constr(min_length=1)] = None
    date: Optional[date] = None


class ExpenseResponse(BaseOrmModel):
    id: int
    title: str
    amount: Decimal
    category: str
    date: date


# Summary schema for dashboard totals
class CategorySummary(BaseOrmModel):
    category: str
    total: Decimal
