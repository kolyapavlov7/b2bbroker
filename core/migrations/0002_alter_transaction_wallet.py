# Generated by Django 3.2 on 2022-06-28 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='core.wallet', verbose_name='Кошелек'),
        ),
    ]