# Generated by Django 5.0.3 on 2024-05-11 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_alter_orderhistory_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
