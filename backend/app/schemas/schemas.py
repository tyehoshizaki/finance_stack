from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import datetime, date

from app.core.constants import MAX_PAGE_SIZE, NAME_MAX_LENGTH, CATEGORY_MAX_LENGTH, DESCRIPTION_MAX_LENGTH, MIN_AMOUNT_TICKS, DEFAULT_SORT_BY, DEFAULT_SORT_ORDER
from app.core.types import TransactionType, SortBy, SortOrder

class TransactionFilters(BaseModel):
    category: str | None = Field(default=None, min_length=1, max_length=CATEGORY_MAX_LENGTH)
    transaction_type: TransactionType | None = None
    min_amount: int | None = Field(default=None, ge=MIN_AMOUNT_TICKS)
    max_amount: int | None = Field(default=None, ge=MIN_AMOUNT_TICKS)
    first_date: date | None = None
    last_date: date | None = None
    
    sort_by: SortBy = DEFAULT_SORT_BY
    sort_order: SortOrder = DEFAULT_SORT_ORDER

    @model_validator(mode="after")
    def validate_amounts(self):
        if self.min_amount is not None and self.max_amount is not None and self.min_amount > self.max_amount:
            raise ValueError("min_amount cannot be greater than max_amount")
        
        return self

    @model_validator(mode="after")
    def validate_dates(self):
        if self.first_date is not None and self.last_date is not None and self.first_date > self.last_date:
            raise ValueError("first_date cannot be greater than last_date")
        
        return self

class TransactionSummary(BaseModel):
    total_income: int = Field(ge=0)
    total_expense: int = Field(ge=0)
    total_transfer: int = Field(ge=0)
    net_balance: int
    transaction_count: int = Field(ge=0)

class TransactionBase(BaseModel):
    name: str = Field(min_length=1, max_length=NAME_MAX_LENGTH)
    amount: int = Field(ge=MIN_AMOUNT_TICKS)
    category: str = Field(min_length=1, max_length=CATEGORY_MAX_LENGTH)
    transaction_type: TransactionType
    description: str | None = Field(default=None, max_length=DESCRIPTION_MAX_LENGTH)
    transaction_date: date
    merchant: str | None = Field(default=None, max_length=NAME_MAX_LENGTH)

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=NAME_MAX_LENGTH)
    amount: int | None = Field(default=None, ge=MIN_AMOUNT_TICKS)
    category: str | None = Field(default=None, min_length=1, max_length=CATEGORY_MAX_LENGTH)
    transaction_type: TransactionType | None = None
    description: str | None = Field(default=None, max_length=DESCRIPTION_MAX_LENGTH)
    transaction_date: date | None = None
    merchant: str | None = Field(default=None, max_length=NAME_MAX_LENGTH)
    
class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    last_updated: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
    
class PaginatedTransactionsResponse(BaseModel):
    items: list[TransactionResponse]

    page: int = Field(ge=0)
    page_size: int = Field(ge=1, le=MAX_PAGE_SIZE)

    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=1)

    has_next: bool
    has_previous: bool