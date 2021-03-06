# Generated by Django 3.1.2 on 2020-12-25 17:22

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20201225_2043'),
        ('chat', '0003_auto_20201202_0114'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chat',
            name='opening_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.openingmessage'),
        ),
        migrations.AddField(
            model_name='chat',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
