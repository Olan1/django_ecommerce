from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product
# Used to generate search query (allows use of or functionality in DB filtering)
from django.db.models import Q


# Create your views here.
def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Product.objects.all()
    query = None
    
    # If search form submits GET request
    if request.GET:
        # q is the name of search input
        if 'q' in request.GET:
            query = request.GET['q']
            # If search input (q) is blank
            if not query:
                messages.error(request, "You didn't enter any search criteria")
                # Redirect to products url
                return redirect(reverse('products'))
            
            # Checks if object in DB contains search query in either the item name or description fields
            # | is the or statement
            #  The i before contains makes the query case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
    
    context = {
        'products': products,
        'search_term': query,
    }
    
    return render(request, 'products/products.html', context)
    
    
def product_detail(request, product_id):
    # del request.session['cart']
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}

    return render(request, 'products/product_detail.html', context)