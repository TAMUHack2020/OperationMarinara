# Twilio and Flask, 1/25/20

from flask import Flask, request, redirect
from twilio import twiml			# Twilio Markup Language

app = Flask(__name__)

@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
	"""Response to incoming calls with a simple text message."""
	
	resp = twiml.Response()
	resp.message("Coronavirus detected in Gate 21")

	return str(resp)

@app.route("/")
def index():
	return "<h1>Welcome to Operation Marinara</h1>"

if __name__ == "__main__":
	app.run(debug=True)
