from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import Product, Category
# Used to generate search query (allows use of or functionality in DB filtering)
from django.db.models import Q


# Create your views here.
def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Product.objects.all()
    query = None
    categories = None
    
    # If search form submits GET request
    if request.GET:
        
        # Check if category is in request URL
        if 'category' in request.GET:
            # Split the category parameter value at the comma
            categories = request.GET['category'].split(',')
            # Filter products by category name which appears in categories list
            products = products.filter(category__name__in=categories)
            # Filter categories in DB down to categories in the URL list
            # This is done so the category objects fields can be accessed in the template as opposed to just the category name as text
            categories = Category.objects.filter(name__in=categories)
        
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
        'current_categories': categories,
    }
    
    return render(request, 'products/products.html', context)
    
    
def product_detail(request, product_id):
    # del request.session['cart']
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}

    return render(request, 'products/product_detail.html', context)