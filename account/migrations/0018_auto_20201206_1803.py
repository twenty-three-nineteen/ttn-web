# Generated by Django 3.1.2 on 2020-12-06 14:33

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_auto_20201202_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(default=None, null=True, validators=[account.validators.birth_validation]),
        ),
    ]
