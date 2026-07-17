from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.models import Transaction
from app.schemas.schemas import TransactionCreate, TransactionUpdate, TransactionFilters
from app.utils.pagination import get_offset
from app.core.types import SortBy, SortOrder


def filter_transactions(db: Session, filters: TransactionFilters):

    query = db.query(Transaction)
    
    if filters.category:
        query = query.filter(Transaction.category == filters.category)
    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)
    if filters.min_amount is not None:
        query = query.filter(Transaction.amount >= filters.min_amount)
    if filters.max_amount is not None:
        query = query.filter(Transaction.amount <= filters.max_amount)
    if filters.first_date is not None:
        query = query.filter(Transaction.transaction_date >= filters.first_date)
    if filters.last_date is not None:
        query = query.filter(Transaction.transaction_date <= filters.last_date)

    return query

def get_filtered_transactions(db: Session, filters: TransactionFilters) -> list[Transaction]:

    return filter_transactions(db=db, filters=filters).all()

def sort_transactions(query, sort_by: SortBy, sort_order: SortOrder):

    sorting_columns = {
        SortBy.TRANSACTION_DATE: Transaction.transaction_date,
        SortBy.AMOUNT: Transaction.amount,
        SortBy.CATEGORY: Transaction.category,
        SortBy.TRANSACTION_TYPE: Transaction.transaction_type,
        SortBy.ID: Transaction.id,
        SortBy.NAME: Transaction.name
    }
    
    sorting_column = sorting_columns[sort_by]
    
    if sort_order == SortOrder.ASC:
        primary_sort = sorting_column.asc()
        secondary_sort = Transaction.id.asc()
    elif sort_order == SortOrder.DESC:
        primary_sort = sorting_column.desc()
        secondary_sort = Transaction.id.desc()
        
    if sort_by == SortBy.ID:
        return query.order_by(primary_sort)
    
    return query.order_by(primary_sort, secondary_sort)

def paginate_transactions(db: Session, filters: TransactionFilters, page: int, page_size: int):
    
    query = filter_transactions(db=db, filters=filters)
    query = sort_transactions(query=query, sort_by=filters.sort_by, sort_order=filters.sort_order)

    total_items = query.count()
    offset = get_offset(page=page, page_size=page_size)

    transactions = (
        query
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return transactions, total_items

def get_transaction_by_id(db: Session, transaction_id: int):
    
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: TransactionCreate):
    
    new_transaction = Transaction(**transaction.model_dump())
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction

def update_transaction(db: Session, transaction_id: int, updated_transaction: TransactionUpdate):
    db_transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)
    
    if db_transaction is None:
        return None
    
    update_data = updated_transaction.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
        
    db_transaction.last_updated = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction_by_id(db=db, transaction_id=transaction_id)
    
    if db_transaction is None:
        return None
    
    db.delete(db_transaction)
    db.commit()
    
    return db_transaction