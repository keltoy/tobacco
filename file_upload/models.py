from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class RelevantDocument(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="文件名称", max_length=100, blank=True, default="")
    file = models.FileField(verbose_name="相关文件", upload_to="document")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "相关文件"


class Presentation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="展示名称", max_length=100, blank=True, default="", unique=True)
    content = HTMLField(verbose_name="展示内容")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name = verbose_name_plural = "文字展示"

