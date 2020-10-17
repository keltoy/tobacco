from django.contrib import admin
from regulatory_system.models import Customer, AbnormalFlow, AbnormalFlowDetail, CustomerLatest
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('license_id', 'shop', 'name', 'phone_number', 'address', 'status', 'key_customer')


class CustomerLatestAdmin(admin.ModelAdmin):
    list_display = ('license_id', 'shop', 'name', 'phone_number', 'address', 'status', 'key_customer')


class AbnormalFlowAdmin(admin.ModelAdmin):
    list_display = ('license_id', 'shop', 'flow_direction',
                    'flow_quantity', 'flow_date', 'commercial_type', 'shop_class')


class AbnormalFlowDetailAdmin(admin.ModelAdmin):
    list_display = ('license_id', 'brand_name', 'spray_code',
                    'flow_quantity', 'flow_date', 'code_type')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerLatest, CustomerLatestAdmin)
admin.site.register(AbnormalFlow, AbnormalFlowAdmin)
admin.site.register(AbnormalFlowDetail, AbnormalFlowDetailAdmin)
