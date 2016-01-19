from flask import Flask, render_template
from slacker import Slacker
import os

app = Flask(__name__)

@app.route("/")
def index():
    slack = Slacker(os.getenv('SLACK_TOKEN', ''))
    response = slack.pins.list(os.getenv('SLACK_ROOM', ''))
    return render_template('index.html',lines=response.body['items'],sl=slack)

if __name__ == "__main__":
    app.run()
