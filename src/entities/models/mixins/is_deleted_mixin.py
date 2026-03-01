import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class IsDeletedMixin:
    is_deleted: Mapped[bool] = mapped_column(
        sa.Boolean(), nullable=False, default=False, server_default=sa.false()
    )
