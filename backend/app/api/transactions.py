from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Annotated
from starlette import status

from app.databases.database import get_db
from app.models.models import Transaction
from app.schemas.schemas import PaginatedTransactionsResponse, TransactionCreate, TransactionSummary, TransactionUpdate, TransactionResponse, TransactionFilters
from app.core.constants import CATEGORY_MAX_LENGTH, MIN_AMOUNT_TICKS, MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE, DEFAULT_SORT_BY, DEFAULT_SORT_ORDER
from app.core.types import TransactionType, SortBy, SortOrder
from app.crud.transactions import filter_transactions, get_filtered_transactions, paginate_transactions, get_transaction_by_id, create_transaction, update_transaction, delete_transaction
from app.services.transactions import build_summary, build_pagination

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

def get_transaction_filters(
    category: Annotated[str | None, Query(min_length=1, max_length=CATEGORY_MAX_LENGTH)] = None,
    transaction_type: TransactionType | None = None,
    min_amount: Annotated[int | None, Query(ge=MIN_AMOUNT_TICKS)] = None,
    max_amount: Annotated[int | None, Query(ge=MIN_AMOUNT_TICKS)] = None,
    first_date: date | None = None,
    last_date: date | None = None,
    sort_by: SortBy = Query(default=DEFAULT_SORT_BY),
    sort_order: SortOrder = Query(default=DEFAULT_SORT_ORDER)
) -> TransactionFilters:
    return TransactionFilters(
        category=category,
        transaction_type=transaction_type,
        min_amount=min_amount,
        max_amount=max_amount,
        first_date=first_date,
        last_date=last_date,
        sort_by=sort_by,
        sort_order=sort_order
    )
    
def check_transaction_exists(transaction: Transaction | None) -> Transaction:
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.get("/", response_model=PaginatedTransactionsResponse)
def get_transactions_route(
    db: Session = Depends(get_db),
    filters: TransactionFilters = Depends(get_transaction_filters),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)
    ):
    
    transactions, total_items = paginate_transactions(db=db, filters=filters, page=page, page_size=page_size)
    
    return build_pagination(transactions=transactions, page=page, page_size=page_size, total_items=total_items)

@router.get("/summary", response_model=TransactionSummary)
def get_summary_route(db: Session = Depends(get_db), filters: TransactionFilters = Depends(get_transaction_filters)):
    
    filtered_transactions = get_filtered_transactions(db=db, filters=filters)
    
    return build_summary(transactions=filtered_transactions)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_one_transaction_route(transaction_id: int, db: Session = Depends(get_db)):
    
    transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)

    return check_transaction_exists(transaction=transaction)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction_route(transaction: TransactionCreate, db: Session = Depends(get_db)):
    
    transaction = create_transaction(db=db, transaction=transaction)
    
    return check_transaction_exists(transaction=transaction)


@router.patch("/{transaction_id}/", response_model=TransactionResponse)
def update_transaction_route(transaction_id: int, updated_transaction: TransactionUpdate, db: Session = Depends(get_db)):
    
    transaction = update_transaction(db=db, transaction_id=transaction_id, updated_transaction=updated_transaction)

    return check_transaction_exists(transaction=transaction)


@router.delete("/{transaction_id}/", response_model=TransactionResponse)
def delete_transaction_route(transaction_id: int, db: Session = Depends(get_db)):
    
    transaction = delete_transaction(db=db, transaction_id=transaction_id)

    return check_transaction_exists(transaction=transaction)