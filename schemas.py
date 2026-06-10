from pydantic import BaseModel, EmailStr, constr, root_validator
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
    category_id: Optional[int] = None
    category: Optional[constr(min_length=1)] = None
    date: date  # expects "YYYY-MM-DD" format

    @root_validator
    def require_category(cls, values):
        if values.get("category_id") is None and values.get("category") is None:
            raise ValueError("Either category_id or category must be provided")
        return values


class ExpenseUpdate(BaseModel):
    title: Optional[constr(min_length=1)] = None
    amount: Optional[Decimal] = None
    category_id: Optional[int] = None
    category: Optional[constr(min_length=1)] = None
    date: Optional[date] = None


class ExpenseResponse(BaseOrmModel):
    id: int
    title: str
    amount: Decimal
    category: str
    category_id: Optional[int] = None
    date: date


class CategoryCreate(BaseModel):
    name: constr(min_length=1)


class CategoryResponse(BaseOrmModel):
    id: int
    name: str


# Summary schema for dashboard totals
class CategorySummary(BaseOrmModel):
    category: str
    total: Decimal
