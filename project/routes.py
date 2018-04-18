from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from lxml import html
import requests, numpy
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from scraper import scrape, time_to_seconds
app = Flask(__name__)
api = Api(app)

@app.route('/')
def default():
	data = scrape()
	seconds = time_to_seconds(data['clock'])
	#data['clock'] = seconds
	return render_template('index.html', data=data)
	
game_parser = reqparse.RequestParser()
game_parser.add_argument('away', required=True)
game_parser.add_argument('home', required=True)

class WinProb(Resource):
	
	def get(self):
		args = game_parser.parse_args()
		away = args['away']
		home = args['home']
		data = scrape(away=away, home=home)
		seconds = time_to_seconds(data['clock'])
		test_data = []
		test_data.append(data['awayScores'])
		test_data.append(data['homeScores'])
		test_data.append(seconds)
		td = numpy.array(test_data).astype(float)
		td = td.reshape(1, -1)
		logisticRegr = joblib.load('model.pkl')
		proba = logisticRegr.predict_proba(td)
		return jsonify(proba[0][1])
		
api.add_resource(WinProb, '/winprob')