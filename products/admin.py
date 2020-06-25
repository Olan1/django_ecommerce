from django.contrib import admin
from .models import Product, Category


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    # Tuple which tells admin which fields to display
    list_display = (
            'sku',
            'name',
            'category',
            'price',
            'rating',
            'image',
        )
        
    # Sort products by field (The 'sku' field in this case)
    ordering = ('sku',)
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
            'friendly_name',
            'name',
        )
    
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)