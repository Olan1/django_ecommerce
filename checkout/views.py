from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.

def checkout(request):
    
    # Get users bag session variable
    bag = request.session.get('bag', {})
    
    # If no bag exists, add error message and redirect to products view
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    # Create instance of order form
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_PfxJNroD5ToLLecvAc1ESE0j00ORJuIZpw',
        'client_secret': 'test client secret',
    }
    
    return render(request, template, context)