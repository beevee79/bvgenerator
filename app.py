#!/usr/bin/env python

import urllib
import json
import os
import random

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") == "input.PWDreset":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("email")

        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ%$#!"
        pw_length = 15
        mypw = ""
    
        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]
        print("PWD Result:")
        print(mypw)
        speech = "Password for the id " + zone + " has been reset to " + mypw
        
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "PasswordGenerator"
        }
    elif req.get("result").get("action") == "MyPWDReset.MyPWDReset-custom":
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("MyPWDReset-followup.email")

        alphabet = "0123456789"
        pw_length = 9
        mypw = ""
    
        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            mypw = mypw + alphabet[next_index]
        print("PWD Result:")
        print(mypw)
        speech = "A ticket has been raised with the support team on your behalf. Ticket number for your reference is " + mypw + ". The support team will contact you at " + zone + "."
        
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "TicketGenerator"
        }
    
    else:
    	return{}
    	
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
