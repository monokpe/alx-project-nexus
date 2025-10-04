import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Order

class StripeWebhookView(APIView):
    """
    An endpoint to receive and process webhooks from Stripe.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            order_id = payment_intent['metadata'].get('order_id')

            if order_id:
                try:
                    order = Order.objects.get(id=order_id)
                    if order.status == Order.OrderStatus.PENDING:
                        order.status = Order.OrderStatus.PROCESSING
                        order.save()
                except Order.DoesNotExist:
                    # The order ID in the metadata does not exist
                    return Response(status=status.HTTP_404_NOT_FOUND)

        # Other event types can be handled here

        return Response(status=status.HTTP_200_OK)
