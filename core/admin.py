from django.contrib import admin
from .models import Category,Momo


# Register your models here.
admin.site.register(Category)
@admin.register(Momo)
class MomoAdmin(admin.ModelAdmin):
    list_display=['id', 'desc', 'price', 'image']
