# Generated by Django 5.0.6 on 2024-07-09 11:55

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medicines', '0004_alter_medicine_price_alter_medicine_remaining'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('medicine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='medicines.medicine')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Inventories',
            },
        ),
    ]
