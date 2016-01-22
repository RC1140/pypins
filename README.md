Currently hosted @ https://pypin.herokuapp.com/

To run your own board:

Clone the repo.            
Get an api key from here (https://api.slack.com/web)  and save it in your SLACK\_TOKEN env variable.                  
Get a room id from here (https://api.slack.com/methods/channels.list/test) and save it in your SLACK\_ROOM env variable.              

Start the app using python app.py or gunicorn app:app
