from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from auth import get_current_user
import models, schemas

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.post("/", response_model=schemas.ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Creates an expense owned by the current user."""
    new_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        user_id=current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=list[schemas.ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    # Optional filters — None means "don't filter by this"
    month: int = None,
    year: int = None,
    category: str = None
):
    """
    Returns expenses for the current user.
    Optionally filter by month, year, or category.
    """
    query = db.query(models.Expense).filter(
        models.Expense.user_id == current_user.id
    )

    # Apply filters only if provided
    if month:
        query = query.filter(
            func.extract("month", models.Expense.date) == month
        )
    if year:
        query = query.filter(
            func.extract("year", models.Expense.date) == year
        )
    if category:
        query = query.filter(models.Expense.category == category)

    # Most recent expenses first
    return query.order_by(models.Expense.date.desc()).all()


@router.get("/summary", response_model=list[schemas.CategorySummary])
def get_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
    month: int = None,
    year: int = None
):
    """
    Returns total spent per category.
    Used to power the dashboard charts.
    """
    query = db.query(
        models.Expense.category,
        func.sum(models.Expense.amount).label("total")
    ).filter(models.Expense.user_id == current_user.id)

    if month:
        query = query.filter(
            func.extract("month", models.Expense.date) == month
        )
    if year:
        query = query.filter(
            func.extract("year", models.Expense.date) == year
        )

    results = query.group_by(models.Expense.category).all()

    return [
        {"category": row.category, "total": row.total}
        for row in results
    ]


@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    updated: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    expense.title = updated.title
    expense.amount = updated.amount
    expense.category = updated.category
    expense.date = updated.date
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id,
        models.Expense.user_id == current_user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return None