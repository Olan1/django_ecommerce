/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/stripe-js
    
    CSS from here:
    https://stripe.com/docs/stripe-js
*/

// Get stripe public key and client secret from the template. Remove the quotation marks by slicing the first and last characters
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// Setup stripe
var stripe = Stripe(stripePublicKey)

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


// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
  var errorDiv = document.getElementById('card-errors');
  if(event.error) {
    var html = `
      <span class="icon" role="alert">
        <i class="fas fa-times"></i>
      </span>
      <span>${ event.error.message }</span>
      `;
    $(errorDiv).html(html);
  } else {
    errorDiv.textContent = '';
  }
});



/*
  Handle form submit
*/

// Get form element
var form = document.getElementById('payment-form');

// Add event listener to form element
form.addEventListener('submit', function(ev) {
  // Prevent default action
  ev.preventDefault();
  // Disable card element and submit button to prevent multiple submissions
  card.update({'disabled': true});
  $('#submit-button').attr('disabled', true);
  
  $('#payment-form').fadeToggle(100);
  $('#loading-overlay').fadeToggle(100);
  
  
  var saveInfo = Boolean($('#id-save-info').attr('checked'));
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
    'save_info': saveInfo
  };
  var url = '/checkout/cache_checkout_data/';
  
  $.post(url, postData).done(function() {
    // Send card info securely to Stripe
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: $.trim(form.full_name.value),
          phone: $.trim(form.phone_number.value),
          email: $.trim(form.email.value),
          address: {
            line1: $.trim(form.street_address1.value),
            line2: $.trim(form.street_address2.value),
            city: $.trim(form.town_or_city.value),
            country: $.trim(form.country.value),
            state: $.trim(form.county.value),
          }
        }
      },
      shipping: {
        name: $.trim(form.full_name.value),
        phone: $.trim(form.phone_number.value),
        address: {
          line1: $.trim(form.street_address1.value),
          line2: $.trim(form.street_address2.value),
          city: $.trim(form.town_or_city.value),
          country: $.trim(form.country.value),
          postal_code: $.trim(form.postcode.value),
          state: $.trim(form.county.value),
        }
      }
    // Then execute this function on result
    }).then(function(result) {
      if (result.error) {
        // Get error div element
        var errorDiv = document.getElementById('card-errors');
        // Show error to your customer (e.g., insufficient funds)
        var html = `
          <span class="icon" role="alert">
            <i class="fas fa-times"></i>
          </span>
          <span>${ result.error.message }</span>`;
        $(errorDiv).html(html);
        
        $('#payment-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);
        
        // Reenable card element and submit button to allow user to fix error and resubmit
        card.update({'disabled': false});
        $('#submit-button').attr('disabled', false);
      } else {
        // If the payment has been processed successfully, submit the form
        if (result.paymentIntent.status === 'succeeded') {
          form.submit();
        }
      }
    });
  }).fail(function () {
    // Just reload page, error will be in django messagess
    location.reload();
  });
});