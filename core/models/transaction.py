from django.db import models
from uuid import uuid4

__all__ = ('Transaction', )


class Transaction(models.Model):
    wallet = models.ForeignKey(
        'core.Wallet',
        verbose_name='Кошелек',
        on_delete=models.PROTECT,
        related_name='transactions'
    )

    tx_id = models.UUIDField(
        'Идентификатор транзакции',
        unique=True,
        default=uuid4
    )

    amount = models.DecimalField(
        'Сумма',
        max_digits=32,
        decimal_places=18
    )

