# Generated by Django 3.1.2 on 2020-10-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulatory_system', '0002_auto_20201013_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(default='有效', max_length=10, verbose_name='客户状态'),
        ),
        migrations.AlterField(
            model_name='customerlatest',
            name='status',
            field=models.CharField(default='有效', max_length=10, verbose_name='客户状态'),
        ),
    ]
