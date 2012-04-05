import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml
import logging
from twilio.rest import TwilioRestClient



DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


numbers = set()
projects = [{"name": "Jesse, Mark and Brennen's Project", "descr":"An awesome project!", "votes":3}]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/list')
def list():
    return jsonify(projects=projects)

@app.route('/vote', methods=['POST'])
def vote():
    from_number = request.args.get('From', None)
    client = TwilioRestClient(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])
    app.logger.debug("Number is " + from_number)
    # number exists
    if from_number in numbers:
        message = client.sms.messages.create(to=from_number,from_="+14156589963",body="Thanks, but you already voted!")
    else:
        body = request.args.get('Body', '')
        letters = "ABCDEFGHIJKLMNOP"
        ident = letters.find(body.strip())
        if ident == -1 or ident >= len(projects):
            message = client.sms.messages.create(to=from_number,from_="+14156589963",body="That is an invalid vote, please try again!")
        else:
            projects[ident]['votes'] += 1
            numbers.add(from_number)
            message = client.sms.messages.create(to=from_number,from_="+14156589963",body="Thank you for your vote!")
    return 'Thank you!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
