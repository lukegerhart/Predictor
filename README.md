# Predictor

## Installation

Make sure python 3.6+ is installed.

Clone/fork the repo then `cd` to the repo.

`cd Predictor` 

### virtualenv

I recommend using virtualenv.

`pip install virtualenv`

Create a new virtual environment.

`virtualenv venv`

### Dependencies

Once virtualenv has completed, activate it.

`venv\Scripts\activate`

Then install python dependencies. This might take a while.

`pip install -r requirements.txt`

## Running the server

Now `cd` to the project.

`cd project`

Set environment variables for flask.

`set FLASK_APP=routes.py`

Optionally, you may run it in debug mode.

`set FLASK_DEBUG=1`

Now run the flask server.

`flask run`

## Using it

Open up git bash or some other console and ping the server.

`curl 127.0.0.1:5000/`

This will return some HTML if everything worked. To get live in-game predictions:

`curl 127.0.0.1:5000/games`

This will return JSON with the status of current NBA games and the win probability of the home team.