from app.models.models import Transaction
from app.schemas.schemas import TransactionSummary
from app.utils.pagination import get_total_pages, get_offset


def build_summary(transactions: list[Transaction]) -> TransactionSummary:
    summary = {
        "total_income": 0,
        "total_expense": 0,
        "total_transfer": 0,
        "net_balance": 0,
        "transaction_count": 0
    }
    
    for transaction in transactions:
        type_lower = transaction.transaction_type.lower()
        if type_lower == "income":
            summary["total_income"] += transaction.amount
        elif type_lower == "expense":
            summary["total_expense"] += transaction.amount
        elif type_lower == "transfer":
            summary["total_transfer"] += transaction.amount
            
    summary["net_balance"] = summary["total_income"] - summary["total_expense"]
    summary["transaction_count"] = len(transactions)
    
    return TransactionSummary(**summary)

def build_pagination(transactions: list[Transaction], page: int, page_size: int, total_items: int) -> dict:
    total_pages = get_total_pages(total_items=total_items, page_size=page_size)
    
    return {
        "items": transactions,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": total_pages > 0 and page > 1
    }