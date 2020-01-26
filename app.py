import user, logging
from flask import Flask, request, render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
app = Flask(__name__)

 # Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

passanger = []

with open("config.json") as jsonFile:
    data = json.load(jsonFile)

client = Client(data["SID"], data["token"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendsms', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if 'mr.bot' in incoming_msg:
        msg.body('hello stupid')    
    else:
        msg.body('fuck')
    return str(resp)

@app.route('/Check-In', methods=['GET','POST'])
def check_in():
    newUser = user.User()
    newUser.name = request.form['Name']
    newUser.phone = request.form['Numba']
    newUser.departureTime = request.form['Departure']
    newUser.arrivalTime = request.form['Arrival']
    newUser.origin = request.form['Origin']
    newUser.destination = request.form['Destination']

    passanger.append(newUser)
    #app.logger.error('%s name', passanger[len(passanger)-1].name)

    message = client.messages \
    .create(
         body='Howdy, {0}, Thank you for flying with American Airlines. Your flight number is {1}, leaves at time {2}, from {3} to {4} at time {5}.'.format(
             newUser.name, 21, newUser.departureTime, newUser.origin, newUser.destination, newUser.arrivalTime),
         from_=data["BotNumba"],
         to=newUser.phone
     )

    return render_template('checkIn.html')

if __name__ == "__main__":
    app.run(debug=True)