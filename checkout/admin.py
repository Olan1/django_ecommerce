from django.contrib import admin
from .models import Order, OrderLineItem


# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    
    inlines = (OrderLineItemAdminInline,)
    
    # Declare read only fields
    readonly_fields = ('order_number', 'date',
                        'delivery_cost', 'order_total',
                        'grand_total',)
    
    # Specify order of fields
    fields = ('order_number', 'date', 'full_name',
                'email', 'phone_number', 'country',
                'postcode', 'town_or_city', 'street_address1',
                'street_address2', 'county', 'delivery_cost',
                'order_total', 'grand_total', )
    
    # Restrict columns that show up in order list to only a few key items
    list_display = ('order_number', 'date', 'full_name',
                    'delivery_cost', 'order_total', 'grand_total', )
                    
    # Specify ordering (by date, with most recent orders at the top)
    ordering = ('-date',)
    

# Register models in admin
admin.site.register(Order, OrderAdmin)