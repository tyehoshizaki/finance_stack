# app/constants.py
from app.core.types import SortBy, SortOrder

NAME_MAX_LENGTH = 255
CATEGORY_MAX_LENGTH = 255
DESCRIPTION_MAX_LENGTH = 255

MIN_AMOUNT_TICKS = 0

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 10

DEFAULT_SORT_BY = SortBy.TRANSACTION_DATE
DEFAULT_SORT_ORDER = SortOrder.DESC

# Money storage rule:
# Store money as integer ticks.
# Example: 1 tick = 1, $0.01 = 100, $1.00 = 10000, $10.99 = 109900
AMOUNT_UNIT = "hundredths of a cent"
TICKS_PER_DOLLAR = 10000