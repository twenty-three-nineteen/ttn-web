# Generated by Django 3.1.2 on 2020-12-17 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20201217_1317'),
        ('chat', '0003_auto_20201202_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='opening_message',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.openingmessage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='status',
            field=models.CharField(default='waiting_for_members', max_length=20),
        ),
    ]
