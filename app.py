import user, logging, flights
from flask import Flask, request, render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse
import json
app = Flask(__name__)

 # Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

passanger = []
questions = {
    "departure": "Check departure time",
    "flight number": "Check flight number",
    "gate number": "Check gate number"
}
questionStr = ""
for key in questions.keys():
    questionStr += key + ": " + questions[key] + "\n"

with open("config.json") as jsonFile:
    data = json.load(jsonFile)

client = Client(data["SID"], data["token"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkin', methods=['GET','POST'])
def check_in():
    newUser = user.User()
    newflight = flights.flight()

    newUser.name = request.form['Name']
    newUser.phone = request.form['Numba']  
    ##generate random number   
    newflight.country = request.form['country']
    newflight.city = request.form['city']
    newflight.state = request.form['state']
    newflight.departureTime = request.form['Departure']
    newflight.arrivalTime = request.form['Arrival']
    
    newUser.flight = newflight
    passanger.append(newUser)

    message = client.messages \
    .create(
         body='Howdy, {0}, Thank you for flying with Operation Marinara. Your flight number is {1}, leaves at time {2}, arrives to {3}, {4} at time {5}.\n List of available commands:\n {6}'.format(
             newUser.name, 21, newflight.departureTime, newflight.city, newflight.state,  newflight.arrivalTime, questionStr),
         from_=data["BotNumba"],
         to=newUser.phone
    )
    overSizeBag = 'https://www.aa.com/i18n/travel-info/baggage/checked-baggage-policy.jsp'
    message = client.messages \
    .create(
         body='Operation Marinara has fees and seasonal limitations for checking bags. Follow this link to make sure your bags fall under the guidelines:{0}'.format(
             overSizeBag),
         from_=data["BotNumba"],
         to=newUser.phone
     )
    return render_template('checkIn.html')

@app.route('/sendsms', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    number = request.form['From']
    flight = flights.flight()

    if len(passanger) < 1:
        msg.body("You're not checked in for a flight with Operation Marinara.")
        return str(resp)

    for p in passanger:
        if p.phone == number:
            flight = p.flight
        else:
            msg.body("You're not checked in for a flight with Operation Marinara.")
            return str(resp)

    if incoming_msg == "departure" or incoming_msg == "Departure":
        msg.body("Depature time at {0}".format(flight.departureTime))
    elif incoming_msg == "gate number" or incoming_msg == "Gate number":
        msg.body("Gate number: {0}".format(21))
    elif incoming_msg == "flight number" or incoming_msg == "Flight number":
        msg.body("Flight number: {0}".format(776))
    else:
        msg.body("I don't understand that question")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)