
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

import stripe

from api.users import get_db
from services.users import supply_credits
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
    # TODO add user_id in the schema
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
            success_url=YOUR_DOMAIN + '/payment-success',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
            metadata={
                "user_id": "12345",
                "product_id": product_schema.id
            }
        )
    except Exception as e:
        return str(e)

    return checkout_session.url


@router.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_db)):
    event = None
    data = await request.body()
    webhook_secret = "whsec_35872817661073cce55f58215a81ee0e31852179490f6dbca6c3c055d3e3007c"
    sig_header = request.headers["stripe-signature"]

    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=sig_header,
            secret=webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        metadata = payment_intent.metadata
        print(metadata)
        print(payment_intent)
        print("Payment successful !")
        # supply_credits(metadata.user_id, metadata.product_id)
    else:
        print('Unhandled event type {}'.format(event['type']))
    session.commit()

    # return jsonify(success=True)