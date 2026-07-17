from enum import StrEnum


class TransactionType(StrEnum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


TRANSACTION_TYPE_CHOICES = [item.value for item in TransactionType]
TRANSACTION_TYPE_MAX_LENGTH = max(len(choice) for choice in TRANSACTION_TYPE_CHOICES)


class SortBy(StrEnum):
    TRANSACTION_DATE = "transaction_date"
    AMOUNT = "amount"
    CATEGORY = "category"
    TRANSACTION_TYPE = "transaction_type"
    ID = "id"
    NAME = "name"

class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"