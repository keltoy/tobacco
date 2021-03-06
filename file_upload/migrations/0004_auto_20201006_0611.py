# Generated by Django 3.1.2 on 2020-10-06 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload', '0003_auto_20201006_0521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='presentation',
            options={'ordering': ('id',), 'verbose_name': '文字展示', 'verbose_name_plural': '文字展示'},
        ),
        migrations.AlterField(
            model_name='presentation',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100, unique=True, verbose_name='展示名称'),
        ),
    ]
