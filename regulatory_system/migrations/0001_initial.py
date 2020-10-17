# Generated by Django 3.1.2 on 2020-10-13 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbnormalFlow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.CharField(blank=True, default='', max_length=12, verbose_name='许可证号')),
                ('shop', models.CharField(blank=True, default='', max_length=100, verbose_name='客户名称')),
                ('shop_class', models.IntegerField(choices=[(0, '无'), (1, '一档'), (2, '二档'), (3, '三档'), (4, '四档'), (5, '五档'), (6, '六档'), (7, '七档'), (8, '八档'), (9, '九档'), (10, '十档'), (11, '十一档'), (12, '十二档'), (13, '十三档'), (14, '十四档'), (15, '十五档'), (16, '十六档'), (17, '十七档'), (18, '十八档'), (19, '十九档'), (20, '二十档')], default=0, verbose_name='客户档位')),
                ('commercial_type', models.CharField(blank=True, default='', max_length=20, verbose_name='经营业态')),
                ('flow_date', models.DateField(blank=True, verbose_name='外流月份')),
                ('flow_direction', models.IntegerField(choices=[(0, ''), (1, '本区'), (2, '外区'), (3, '外省')], default=0, verbose_name='流向')),
                ('flow_quantity', models.FloatField(default=0, verbose_name='真烟数量')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '流动信息',
                'verbose_name_plural': '流动信息',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='AbnormalFlowDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.CharField(blank=True, default='', max_length=12, verbose_name='许可证号')),
                ('brand_name', models.CharField(blank=True, default='', max_length=50, verbose_name='品牌名称')),
                ('flow_quantity', models.FloatField(default=0, verbose_name='数量')),
                ('spray_code', models.CharField(blank=True, default='', max_length=32, verbose_name='32位喷码')),
                ('code_type', models.CharField(default='有效', max_length=10, verbose_name='类型')),
                ('flow_date', models.DateField(blank=True, verbose_name='外流月份')),
                ('shop', models.CharField(blank=True, default='', max_length=100, verbose_name='客户名称')),
                ('flow_direction', models.IntegerField(choices=[(0, ''), (1, '本区'), (2, '外区'), (3, '外省')], default=0, verbose_name='流向')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '流动详情',
                'verbose_name_plural': '流动详情',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.CharField(blank=True, default='', max_length=12, verbose_name='许可证号')),
                ('shop', models.CharField(blank=True, default='', max_length=100, verbose_name='客户名称')),
                ('name', models.CharField(blank=True, default='', max_length=10, verbose_name='负责人名称')),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, verbose_name='负责人电话')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='营业地址')),
                ('order_phone', models.CharField(blank=True, default='', max_length=20, verbose_name='订货电话')),
                ('status', models.CharField(default='无效', max_length=10, verbose_name='客户状态')),
                ('commercial_type', models.CharField(blank=True, default='', max_length=20, verbose_name='经营业态')),
                ('shop_class', models.IntegerField(choices=[(0, '无'), (1, '一档'), (2, '二档'), (3, '三档'), (4, '四档'), (5, '五档'), (6, '六档'), (7, '七档'), (8, '八档'), (9, '九档'), (10, '十档'), (11, '十一档'), (12, '十二档'), (13, '十三档'), (14, '十四档'), (15, '十五档'), (16, '十六档'), (17, '十七档'), (18, '十八档'), (19, '十九档'), (20, '二十档')], default=0, verbose_name='客户档位')),
                ('market_type', models.CharField(blank=True, default='', max_length=20, verbose_name='市场类型')),
                ('order_number', models.IntegerField(default=0, verbose_name='订货次数')),
                ('require_quantity', models.FloatField(default=0, verbose_name='需求数量')),
                ('order_quantity', models.FloatField(default=0, verbose_name='订购数量')),
                ('money_amount', models.FloatField(default=0, verbose_name='金额')),
                ('key_customer', models.BooleanField(default=False, verbose_name='是否大户')),
                ('active_date', models.DateField(blank=True, verbose_name='有效月份')),
                ('import_date', models.DateField(blank=True, verbose_name='导入时间')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '客户信息',
                'verbose_name_plural': '客户信息',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CustomerLatest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('license_id', models.CharField(blank=True, default='', max_length=12, verbose_name='许可证号')),
                ('shop', models.CharField(blank=True, default='', max_length=100, verbose_name='客户名称')),
                ('name', models.CharField(blank=True, default='', max_length=10, verbose_name='负责人名称')),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, verbose_name='负责人电话')),
                ('address', models.CharField(blank=True, default='', max_length=100, verbose_name='营业地址')),
                ('order_phone', models.CharField(blank=True, default='', max_length=20, verbose_name='订货电话')),
                ('status', models.CharField(default='无效', max_length=10, verbose_name='客户状态')),
                ('commercial_type', models.CharField(blank=True, default='', max_length=20, verbose_name='经营业态')),
                ('shop_class', models.IntegerField(choices=[(0, '无'), (1, '一档'), (2, '二档'), (3, '三档'), (4, '四档'), (5, '五档'), (6, '六档'), (7, '七档'), (8, '八档'), (9, '九档'), (10, '十档'), (11, '十一档'), (12, '十二档'), (13, '十三档'), (14, '十四档'), (15, '十五档'), (16, '十六档'), (17, '十七档'), (18, '十八档'), (19, '十九档'), (20, '二十档')], default=0, verbose_name='客户档位')),
                ('market_type', models.CharField(blank=True, default='', max_length=20, verbose_name='市场类型')),
                ('order_number', models.IntegerField(default=0, verbose_name='订货次数')),
                ('require_quantity', models.FloatField(default=0, verbose_name='需求数量')),
                ('order_quantity', models.FloatField(default=0, verbose_name='订购数量')),
                ('money_amount', models.FloatField(default=0, verbose_name='金额')),
                ('key_customer', models.BooleanField(default=False, verbose_name='是否大户')),
                ('active_date', models.DateField(blank=True, verbose_name='有效月份')),
                ('import_date', models.DateField(blank=True, verbose_name='导入时间')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '客户信息缓存',
                'verbose_name_plural': '客户信息缓存',
                'db_table': 'regulatory_system_customerlatest',
                'ordering': ('id',),
            },
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['license_id', 'import_date'], name='regulatory__license_f961df_idx'),
        ),
    ]
