from datetime import datetime

from src.users.models import table_registry
from sqlalchemy.orm import Mapped, mapped_column


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    category: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, default_factory=datetime.now
    )
