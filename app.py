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
        g.users = setup_users()
    if not g.get('channels',None):
        g.channels = setup_channels()

def setup_users():
    immutableUsers =  slack.users.list().body['members']
    userLookup = {}
    for u in immutableUsers:
        userLookup[u['id']] = u['name']
    return userLookup

def setup_channels():
    immutableChannels =  slack.channels.list().body['channels']
    channelLookup = {}
    #We need to store the values in reverse compared to the users since we have a channel name but no id.
    for u in immutableChannels:
        channelLookup[u['name']] = u['id']
    return channelLookup

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
@app.route("/<channel_name>")
def index(channel_name=None):
    channel_id = ''
    if not channel_name and os.getenv('SLACK_ROOM', ''):
        channel_id = os.getenv('SLACK_ROOM', '')
    elif channel_name in g.channels:
        channel_id = g.channels[channel_name]
    else:
        channel_id = g.channels['work-opportunities']
    response = slack.pins.list(channel_id)
    return render_template('index.html',lines=response.body['items'],users=g.users)

if __name__ == "__main__":
    app.run()
