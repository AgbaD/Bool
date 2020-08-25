#!/usr/bin/python
# Author:   @BlankGodd_

from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction

import json

paystack_secret_key = "sk_test_8f26836f53bc11421e081aca7ef21ac222cf4900"
paystack = Paystack(secret_key=paystack_secret_key)

"""Paystack Implementation"""
def new_transaction(email, amount):
    response = Transaction.initialize(
        amount=amount, email=email)
    response =  json.load(response)
    if response["status"]:
        payment_url = response['data']["authorization_url"]
        return True,payment_url
    else:
        return False,""

def verify_transaction(reference):
    resp = Transaction.verify(reference=reference)
    resp = json.load(resp)
    if resp['data']['status'] == "success":
        data = {
            "verify" : True,
            "data" : resp['customer']['metadata']['cart']
            }
        return data 
    return {
        "verify" :False
