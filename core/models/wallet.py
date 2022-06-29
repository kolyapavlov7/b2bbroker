from decimal import Decimal

from django.db import models

from core.managers import WalletManager

__all__ = ('Wallet', )


class Wallet(models.Model):
    default_balance = Decimal('0.0')

    label = models.TextField(
        'Метка',
        blank=True,
        null=True
    )

    balance = models.DecimalField(
        'Баланс',
        max_digits=32,
        decimal_places=18
    )

    objects = WalletManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.balance = self.default_balance

        super(Wallet, self).save(*args, **kwargs)

    @classmethod
    def create(cls, *args, **kwargs):
        obj = cls(**args, **kwargs)
        obj.balance = cls.default_balance
        return obj


