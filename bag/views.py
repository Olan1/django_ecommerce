from django.shortcuts import render, redirect, reverse, HttpResponse

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
    
    
def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    
    # 'quantity' is the value attribute in the form inputs
    quantity = int(request.POST.get('quantity'))
    
    # Get product size from POST request
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    
    # Get the bag session variable if it exists, or create it if not
    bag = request.session.get('bag', {})
    
    # If a product with sizes is being adjusted in the bag
    if size:
        # If quantity is greater than 0, update quantity = new quantity
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        # If quantity is 0, remove item from bag
        else:
            del bag[item_id]['items_by_size'][size]
            # If that is the only size of that item, remove item entirely
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    # If product without sizes is being adjusted in the bag
    else:
        # If quantity is greater than 0, update quantity = new quantity
        if quantity > 0:
            bag[item_id] = quantity
        # If quantity is 0, remove item from bag
        else:
            bag.pop(item_id)
    
    # Overwrite the bag session variable with the updated version
    request.session['bag'] = bag
    
    # Redirect to view_bag view
    return redirect(reverse('view_bag'))
    
    
def remove_from_bag(request, item_id):
    """ Remove item from shopping bag """
    
    try:
        # Get product size from POST request
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        
        # Get the bag session variable if it exists, or create it if not
        bag = request.session.get('bag', {})
        
        # If a product with sizes is being adjusted in the bag
        if size:
            # Delete that size item from bag
            del bag[item_id]['items_by_size'][size]
            # If that is the only size of that item, remove item entirely
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        # If product without sizes is being removed, simply remove the item
        else:
            bag.pop(item_id)
        
        # Overwrite the bag session variable with the updated version
        request.session['bag'] = bag
        
        # Since this view will be posted to by a JS function, return a 200 HTTP response implying item was successfully removed
        return HttpResponse(status=200)
    # If exception occurs, return a 500 http error response
    except Exception as e:
        return HttpResponse(status=500)