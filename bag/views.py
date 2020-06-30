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
    
    # Get the bag session variable if it exists, or create it if not
    bag = request.session.get('bag', {})
    
    # If the item id key already exists within the bag dict, increment its value
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    # If item id key does not exist within dict, create it and add quantity as value
    else:
        bag[item_id] = quantity
    
    # Overwrite the bag session variable with the updated version
    request.session['bag'] = bag
    
    # Redirect to current product item page
    return redirect(redirect_url)