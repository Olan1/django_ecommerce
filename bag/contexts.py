# Decimal is more accurate than float which is succeptable to rounding errors
# Decimal is preffered when working with money because it is more accurate
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    
    bag_items = []
    total = 0
    product_count = 0
    # Get bag session variable if it exists, else initialize it
    bag = request.session.get('bag', {})
    
    # Iterate through item_id's and their quantities in bag (from bag session variable)
    for item_id, item_data in bag.items():
        # If item_data is an integer, item_data is the quantity of the item
        if isinstance(item_data, int):
            # Get product
            product = get_object_or_404(Product, pk=item_id)
            # Add cost of item times its quantity to the total
            total += item_data * product.price
            # Increment thr product count by the quantity of the current iteration item
            product_count += item_data
            # Dict of item id, quantity, and product object
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        # If item_data is not an int, it is a dictionary
        else:
            # Iterate through items inner dictionary (item_data)
            for size, quantity in item_data['items_by_size'].items():
                # Get product
                product = get_object_or_404(Product, pk=item_id)
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })
    
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
        
    grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
    
    return context