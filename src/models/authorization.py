"""Model Autorização."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from communs.base_model import AbstractBaseModel

if TYPE_CHECKING:
    from models.role import Role
    from models.transaction import Transaction

from config.table_registry import table_registry


@table_registry.mapped_as_dataclass
class Authorization(AbstractBaseModel):
    """Representa a autorização de um papel (Role) a uma operação (Transaction)."""  # noqa: E501

    __tablename__ = 'authorization'

    id: Mapped[int] = mapped_column(primary_key=True, name='id')
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False)
    transaction_id: Mapped[int] = mapped_column(
        ForeignKey('transaction.id'), nullable=False,
    )

    role: Mapped['Role'] = relationship(
        back_populates='authorizations', lazy='subquery',
    )
    transaction: Mapped['Transaction'] = relationship(
        back_populates='authorizations', lazy='subquery',
    )

    __table_args__ = (
        Index('idx_role_transaction', role_id, transaction_id, unique=True),
    )
