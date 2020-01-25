# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACd1b6298567a153b756f6764bf9de27c2'
auth_token = '5c9aaf5007e5d6a3120a8c1568f2fe24'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12512548067',
                     to='+12144496966'
                 )

print(message.sid)