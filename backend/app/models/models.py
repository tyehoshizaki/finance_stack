from datetime import date, datetime, timezone
from sqlalchemy import String, DateTime, Date, INT
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.database import Base
from app.core.constants import NAME_MAX_LENGTH, CATEGORY_MAX_LENGTH, DESCRIPTION_MAX_LENGTH
from app.core.types import TRANSACTION_TYPE_MAX_LENGTH


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH), nullable=False)
    amount: Mapped[int] = mapped_column(INT, nullable=False)
    category: Mapped[str] = mapped_column(String(CATEGORY_MAX_LENGTH), nullable=False)
    transaction_type: Mapped[str] = mapped_column(String(TRANSACTION_TYPE_MAX_LENGTH), nullable=False)
    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_MAX_LENGTH), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    merchant: Mapped[str | None] = mapped_column(String(NAME_MAX_LENGTH), nullable=True)