from django.db import models

__all__ = ('WalletManager', )


class WalletManager(models.Manager):
    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        from core.models import Wallet
        for obj in objs:
            obj.balance = Wallet.default_balance
        return super().bulk_create(objs, batch_size=batch_size, ignore_conflicts=ignore_conflicts)
