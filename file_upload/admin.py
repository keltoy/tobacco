from django.contrib import admin
from file_upload.models import RelevantDocument, Presentation

# Register your models here.


class RelevantDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')


class PresentationAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(RelevantDocument, RelevantDocumentAdmin)
admin.site.register(Presentation, PresentationAdmin)
