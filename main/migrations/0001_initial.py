# Generated by Django 4.2 on 2023-11-23 03:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockTransaction',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stock_name', models.CharField(max_length=255)),
                ('bought_at_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('is_sold', models.BooleanField(default=False)),
                ('sold_at_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_transactions', to='accounts.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
