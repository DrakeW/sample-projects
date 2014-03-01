#import Flask functions
from flask import Flask, render_template
from random import randint

#create Flask application
app = Flask(__name__)

#index() will be run when '/' is requested
@app.route('/')
def index():
    #data returned to browser
    return 'Yay first web app!'

@app.route('/random_example')
def random_example():
    return render_template('random.html', random_num=randint(1, 100))

#start the Flask server which listens to requests
app.run(debug=True)
