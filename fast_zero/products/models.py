from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from fast_zero.database import table_registry

@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
    category: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default='CURRENT_TIMESTAMP')