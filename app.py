from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
app = Flask(__name__)

 # Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


with open("config.json") as jsonFile:
    data = json.load(jsonFile)

client = Client(data["SID"], data["token"])

message = client.messages \
    .create(
         body='Howdy, “Name”. Thank you for flying with American Airlines. Your flight number is “Flight Number”, leaves at time “time”, from “place A” to “place B” at time “ETA”.',
         from_=data["BotNumba"],
         to=data["MyNumba"]
     )

@app.route('/', methods=['POST'])

def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if 'mr.bot' in incoming_msg:
        msg.body('hello stupid')    
    else:
        msg.body('fuck')
    return str(resp)