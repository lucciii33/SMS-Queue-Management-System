import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send(body='body', to=''): 
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    sender = os.environ['from_']
    recipient = os.environ['to']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                                body=body,
                                from_=sender,
                                to=recipient
                            )

    print(message.sid)