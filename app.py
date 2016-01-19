from flask import Flask, render_template
from slacker import Slacker
import os

app = Flask(__name__)
slack = Slacker(os.getenv('SLACK_TOKEN', ''))
users = {}

def setup():
    users =  slack.users.list().body['members']
    userLookup = {}
    for u in users:
        userLookup[u['id']] = u['name']
    return userLookup

@app.route("/")
def index():    
    if len(users.keys()) == 0:
        users = setup()
    response = slack.pins.list(os.getenv('SLACK_ROOM', ''))
    return render_template('index.html',lines=response.body['items'],users=users)

if __name__ == "__main__":
    users = setup()
    app.run()
