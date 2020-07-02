from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view to render the contents of the users shopping bag page """
    
    return render(request, 'bag/bag.html')
    
    
def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    
    # 'quantity' and 'redirect_url' are the value attributes in the form inputs
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    
    # Get product size from POST request
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    
    # Get the bag session variable if it exists, or create it if not
    bag = request.session.get('bag', {})
    
    # If a product with sizes is being added to the bag
    if size:
        # If item already in the bag
        if item_id in list(bag.keys()):
            # If item already exists in bag of the same size, increment quantity
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            # If item in bag but different size, add item with new size
            else:
                bag[item_id]['items_by_size'][size] = quantity
        # If item not already in bag, add it as dictionary with sizes
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # If product without sizes is being added to bag
    else:
        # If item already in bag, increment quantity
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        # If item not already in bag, create it with value = quantity
        else:
            bag[item_id] = quantity
    
    # Overwrite the bag session variable with the updated version
    request.session['bag'] = bag
    
    # Redirect to current product item page
    return redirect(redirect_url)