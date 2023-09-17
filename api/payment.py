
from fastapi import APIRouter
from starlette.requests import Request

import stripe

from shemas.product import ProductSchema

stripe.api_key = 'sk_test_51Nqvj5EJAnEEoeUjoBc4MyFufOsTDGu7v8meUImAU0vXmc5uB1UcSJUSXCdO6xX6PpRRZ3DnYpqpqdLNZmA5ownP00aap3cXp8'

router = APIRouter(
    prefix="/payment",
)

YOUR_DOMAIN = 'http://localhost:4200'

product_prices = {
    "product1": "price_1NrHP9EJAnEEoeUjx3ndzZ8Z",
    "product2": "price_1NqvpcEJAnEEoeUjktOzZrIr",
    "product3": "price_1NrHPrEJAnEEoeUjI32rFMbs",
}


@router.post("/create-checkout-session")
def create_checkout_session(product_schema: ProductSchema) -> str:
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': product_prices[product_schema.id],
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return checkout_session.url


@router.post("/webhook")
async def webhook(request: Request):
    event = None
    payload = await request.json()
    endpoint_secret = "whsec_35872817661073cce55f58215a81ee0e31852179490f6dbca6c3c055d3e3007c"
    sig_header = request.headers["stripe-signature"]
    # print(payload)
    print(sig_header)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    #
    # # Handle the event
    # if event['type'] == 'payment_intent.succeeded':
    #   payment_intent = event['data']['object']
    # # ... handle other event types
    # else:
    #   print('Unhandled event type {}'.format(event['type']))
    #
    # return jsonify(success=True)