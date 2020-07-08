/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/stripe-js
    
    CSS from here:
    https://stripe.com/docs/stripe-js
*/

// Get stripe public key and client secret from the template. Remove the quotation marks by slicing the first and last characters
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);

// Setup stripe
var stripe = Stripe(stripe_public_key)

// Create an instance of stripe elements
var elements = stripe.elements();

// CSS for styling card element
var style = {
  base: {
    color: '#000',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#dc3545',
    iconColor: '#dc3545'
  }
};

// Use instance of stripe element to create a card element with style attribute set to style var
var card = elements.create('card', {style: style});

// Mount card element to #card-element div
card.mount('#card-element');