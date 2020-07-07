from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'
    
    # Override ready method to import signals method
    def ready(self):
        import checkout.signals