import urllib
from rottentomatoes import RT
from twilio.rest import TwilioRestClient
import twilio_tokens

from flask import Flask, render_template, request
app = Flask(__name__)

rt = RT()
tw = TwilioRestClient(account=twilio_tokens.ACCOUNT, token=twilio_tokens.TOKEN)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/in_theaters')
def in_theaters():
  movies = rt.movies('in_theaters')
  return render_template('in_theaters.html', movies=movies)

@app.route('/message', methods=['GET'])
def tweets():
  movie = request.args.get('movie')
  numbers = request.args.get('numbers').split(',')
  message = request.args.get('message')
  if not movie:
    return 'ERROR: No movie provided'

  if not numbers or len(numbers) == 0:
    return 'ERROR: No numbers provided'

  if not message or len(message) == 0:
    return 'ERROR: No message provided'
  
  for number in numbers:
    sms = tw.messages.create(to=number, from_=twilio_tokens.NUMBER, body=message)

  return render_template('message.html', movie=movie, numbers=numbers, message=message)

if __name__ == '__main__':
  app.run(debug=True)
