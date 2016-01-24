from flask import Flask, render_template, g
from slacker import Slacker
import os
import datetime

app = Flask(__name__)
app.debug = True
slack = Slacker(os.getenv('SLACK_TOKEN', ''))

@app.before_request
def initialUserLoad():
    if not g.get('users',None):
        g.users = setup()

def setup():
    immutableUsers =  slack.users.list().body['members']
    userLookup = {}
    for u in immutableUsers:
        userLookup[u['id']] = u['name']
    return userLookup

@app.template_filter('tstodt')
def timestamp_to_datetime(s):
    uniqueTsParts = s.split('.')
    if len(uniqueTsParts) > 0:
        return datetime.datetime.fromtimestamp(
            int(uniqueTsParts[0])
        ).strftime('%Y-%m-%d')
    else:
        return datetime.datetime.fromtimestamp(
            int(s)
        ).strftime('%Y-%m-%d')
 

@app.route("/")
def index():    
    response = slack.pins.list(os.getenv('SLACK_ROOM', ''))
    return render_template('index.html',lines=response.body['items'],users=g.users)

if __name__ == "__main__":
    users = setup()
    app.run()
