from django.http import JsonResponse
import stripe
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import stripe.error

@csrf_exempt
@api_view(['POST'])
def payment_view(request):
    """
    Process a payment.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: The JSON response containing the client secret for the payment intent.
        
    Raises:
        stripe.error.StripeError: If any error occurs during the payment processing.

    """
    try:
        amount = request.data.get('amount')  # Get the amount from the request

        stripe.api_key = 'sk_test_51NL6vWB09khdlanwYk9Oj8TTb4CcGr8g9e1NtSlPUbTbO8NK8qtoI5NuUdC4wWakyS8izRKGqxbCPHHz3AprwSgx00VsGzoTli'

            # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )

        return JsonResponse({'client_secret': intent.client_secret})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)}, status=400)

