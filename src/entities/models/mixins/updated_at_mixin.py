import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class UpdatedAtMixin:
    updated_at: Mapped[dt.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        default=dt.datetime.now(dt.UTC),
        server_default=sa.func.now(),
    )
