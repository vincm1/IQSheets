import os
from flask import current_app, Blueprint, redirect, url_for, render_template, request, jsonify, abort
import stripe 

# This is your test secret API key.
stripe.api_key = current_app.config['STRIPE_SECRETKEY_TEST']

YOUR_DOMAIN = 'http://localhost:5000'

stripe_customers = stripe.Subscription.list()
stripe_subscriptions = stripe.Subscription.list()

# @stripe_blueprint.route('/subscriptions')
# def all_subscriptions():
#     """ Generating all Subscriptions """ 
#     subscriptions = stripe.Subscription.list()
#     print(subscriptions)
#     return subscriptions

# @stripe_blueprint('/payment')
# def payment():
#     return render_template('payment.html')
# @stripe_blueprint.route('/create-checkout-session', methods=['POST'])
# def create_checkout_session():
#     try:
#         session = stripe.checkout.Session.create(
#             ui_mode = 'embedded',
#             line_items=[
#                 {
#                     # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
#                     'price': '{{PRICE_ID}}',
#                     'quantity': 1,
#                 },
#             ],
#             mode='payment',
#             return_url=YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',
#             automatic_tax={'enabled': True},
#         )
#     except Exception as e:
#         return str(e)

#     return jsonify(clientSecret=session.client_secret)

# @stripe_blueprint.route('/session-status', methods=['GET'])
# def session_status():
#   session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

#   return jsonify(status=session.status, customer_email=session.customer_details.email)