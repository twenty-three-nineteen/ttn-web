# Generated by Django 3.1.2 on 2020-12-25 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0018_auto_20201206_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='openingmessage',
            name='categories',
            field=models.ManyToManyField(blank=True, default=None, to='account.Interest'),
        ),
        migrations.AddField(
            model_name='openingmessage',
            name='max_number_of_members',
            field=models.IntegerField(blank=True, default=2),
        ),
        migrations.AddField(
            model_name='openingmessage',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
