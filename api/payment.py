
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

import stripe
from starlette.responses import Response

from api.users import get_db
from services.users import supply_credits
from shemas.product import CheckoutMetadataSchema

stripe.api_key = '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'

router = APIRouter(
    prefix="/payment",
)

YOUR_DOMAIN = 'https://coverletterai.io'

product_prices = {
    "product1": "price_1OCSwdEJAnEEoeUj9FBd2pwU",
    "product2": "price_1OCSz5EJAnEEoeUjaImL4SYc",
    "product3": "price_1OCT0REJAnEEoeUjf98OBSUp",
}


@router.post("/create-checkout-session")
def create_checkout_session(metadata_schema: CheckoutMetadataSchema) -> str:
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': product_prices[metadata_schema.product_id],
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment-success',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
            payment_intent_data={
                "metadata": {
                    "user_id": metadata_schema.user_id,
                    "product_id": metadata_schema.product_id,
                }
            }
        )
    except Exception as e:
        return str(e)

    return checkout_session.url


@router.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_db)):
    event = None
    data = await request.body()
    webhook_secret = "whsec_AlJUigC0NWveNR6LZLQttyidwCt4Lg1P"
    sig_header = request.headers["stripe-signature"]

    try:
        event = stripe.Webhook.construct_event(
            payload=data,
            sig_header=sig_header,
            secret=webhook_secret
        )

    except ValueError as e:
        return {"error": str(e)}

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object
        metadata = payment_intent.metadata
        supply_credits(session, metadata.user_id, metadata.product_id)
        print("payment intent success event")
    else:
        print('Unhandled event type {}'.format(event['type']))
    session.commit()

    return {"status": "success"}
