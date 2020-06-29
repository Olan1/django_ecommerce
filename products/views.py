from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
# Used to generate search query (allows use of or functionality in DB filtering)
from django.db.models import Q
from django.db.models.functions import Lower

# Local imports
from .models import Product, Category


# Create your views here.
def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """
    
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    
    # If search form submits GET request
    if request.GET:
        
        # Check if sort parameter in url get request
        if 'sort' in request.GET:
            # Set sortkey var to sort parameter value
            sortkey = request.GET['sort']
            # Set sort var = sortkey to preserve parameter value
            sort = sortkey
            
            # If user is sorting by name field
            if sortkey == 'name':
                # Set sortkey = new annotated field lower_name
                sortkey = 'lower_name'
                # Annotate current list of products with new field(lower_name) and set products = lower_case (the lowercase version of the 'name' field)
                products = products.annotate(lower_name=Lower('name'))
            
            # If sort key is = category
            if sortkey == 'category':
                # Sort = the category model name field -> Order by category name (eg: activewear, jeans - A-Z)
                sortkey = 'category__name'
            
            # Check if direction parameter defined
            if 'direction' in request.GET:
                # Get direction value
                direction = request.GET['direction']
                
                # If direction is descending, reverse the order of the sortkey
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            
            products = products.order_by(sortkey)
        
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
    
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/products.html', context)
    
    
def product_detail(request, product_id):
    # del request.session['cart']
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}

    return render(request, 'products/product_detail.html', context)