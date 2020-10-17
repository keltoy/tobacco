from django.db import models

# Create your models here.
CUSTOMER_SHOP_CLASS_CHOICES = [
    (0, "无"),
    (1, "一档"),
    (2, "二档"),
    (3, "三档"),
    (4, "四档"),
    (5, "五档"),
    (6, "六档"),
    (7, "七档"),
    (8, "八档"),
    (9, "九档"),
    (10, "十档"),
    (11, "十一档"),
    (12, "十二档"),
    (13, "十三档"),
    (14, "十四档"),
    (15, "十五档"),
    (16, "十六档"),
    (17, "十七档"),
    (18, "十八档"),
    (19, "十九档"),
    (20, "二十档"),

]

FLOW_DIRECTION_CHOICES = [
    (0, ""),
    (1, "本区"),
    (2, "外区"),
    (3, "外省"),
]


class AbnormalFlow(models.Model):
    id = models.AutoField(primary_key=True)
    license_id = models.CharField(max_length=12, blank=True, default="", verbose_name="许可证号")
    shop = models.CharField(max_length=100, blank=True, default="", verbose_name="客户名称")
    shop_class = models.IntegerField(choices=CUSTOMER_SHOP_CLASS_CHOICES, default=0, verbose_name="客户档位")
    commercial_type = models.CharField(max_length=20, blank=True, default="", verbose_name="经营业态")
    flow_date = models.DateField(blank=True, verbose_name="外流月份")
    flow_direction = models.IntegerField(choices=FLOW_DIRECTION_CHOICES, default=0, verbose_name="流向")
    flow_quantity = models.FloatField(default=0, verbose_name="真烟数量")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "流动信息"


class AbnormalFlowDetail(models.Model):
    id = models.AutoField(primary_key=True)
    license_id = models.CharField(max_length=12, blank=True, default="", verbose_name="许可证号")
    brand_name = models.CharField(max_length=50, blank=True, default="", verbose_name="品牌名称")
    flow_quantity = models.FloatField(default=0, verbose_name="数量")
    spray_code = models.CharField(max_length=32, blank=True, default="", verbose_name="32位喷码")
    code_type = models.CharField(max_length=10, blank=False, default="有效", verbose_name="类型")
    flow_date = models.DateField(blank=True, verbose_name="外流月份")
    shop = models.CharField(max_length=100, blank=True, default="", verbose_name="客户名称")
    flow_direction = models.IntegerField(choices=FLOW_DIRECTION_CHOICES, default=0, verbose_name="流向")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "流动详情"


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    license_id = models.CharField(max_length=12, blank=True, default="", verbose_name="许可证号")
    shop = models.CharField(max_length=100, blank=True, default="", verbose_name="客户名称")
    name = models.CharField(max_length=10, blank=True, default="", verbose_name="负责人名称")
    phone_number = models.CharField(max_length=20, blank=True, default="", verbose_name="负责人电话")
    address = models.CharField(max_length=100, blank=True, default="", verbose_name="营业地址")
    order_phone = models.CharField(max_length=20, blank=True, default="", verbose_name="订货电话")
    status = models.CharField(max_length=10, blank=False, default="有效", verbose_name="客户状态")
    commercial_type = models.CharField(max_length=20, blank=True, default="", verbose_name="经营业态")
    shop_class = models.IntegerField(choices=CUSTOMER_SHOP_CLASS_CHOICES, default=0, verbose_name="客户档位")
    market_type = models.CharField(max_length=20, blank=True, default="", verbose_name="市场类型")
    order_number = models.IntegerField(default=0, verbose_name="订货次数")
    require_quantity = models.FloatField(default=0, verbose_name="需求数量")
    order_quantity = models.FloatField(default=0, verbose_name="订购数量")
    money_amount = models.FloatField(default=0, verbose_name="金额")
    key_customer = models.BooleanField(default=False, verbose_name="是否大户")
    active_date = models.DateField(blank=True, verbose_name="有效月份")
    import_date = models.DateField(blank=True, verbose_name="导入时间")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "客户信息"

class CustomerLatest(models.Model):
    id = models.AutoField(primary_key=True)
    license_id = models.CharField(max_length=12, blank=True, default="", verbose_name="许可证号")
    shop = models.CharField(max_length=100, blank=True, default="", verbose_name="客户名称")
    name = models.CharField(max_length=10, blank=True, default="", verbose_name="负责人名称")
    phone_number = models.CharField(max_length=20, blank=True, default="", verbose_name="负责人电话")
    address = models.CharField(max_length=100, blank=True, default="", verbose_name="营业地址")
    order_phone = models.CharField(max_length=20, blank=True, default="", verbose_name="订货电话")
    status = models.CharField(max_length=10, blank=False, default="有效", verbose_name="客户状态")
    commercial_type = models.CharField(max_length=20, blank=True, default="", verbose_name="经营业态")
    shop_class = models.IntegerField(choices=CUSTOMER_SHOP_CLASS_CHOICES, default=0, verbose_name="客户档位")
    market_type = models.CharField(max_length=20, blank=True, default="", verbose_name="市场类型")
    order_number = models.IntegerField(default=0, verbose_name="订货次数")
    require_quantity = models.FloatField(default=0, verbose_name="需求数量")
    order_quantity = models.FloatField(default=0, verbose_name="订购数量")
    money_amount = models.FloatField(default=0, verbose_name="金额")
    key_customer = models.BooleanField(default=False, verbose_name="是否大户")
    active_date = models.DateField(blank=True, verbose_name="有效月份")
    import_date = models.DateField(blank=True, verbose_name="导入时间")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "客户信息缓存"
        db_table = "regulatory_system_customerlatest"
