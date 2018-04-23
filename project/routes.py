from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api, reqparse
from lxml import html
import requests, numpy
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib
from scraper import scrape, time_to_seconds
app = Flask(__name__)
api = Api(app)

def get_data():
	# data = scrape()
	# seconds = time_to_seconds(data['clock'])
	# data['seconds'] = seconds
	# return data
	
	# Use this for when there are no live games
	seconds = time_to_seconds(['4th | 8:15', '3rd | 4:20'])
	return {'clock':['4th | 8:15', '3rd | 4:20'], 'awayTeams':['MIA', 'MIN'], 'awayScores':[50, 89], 'homeTeams': ['PHI', 'HOU'], 'homeScores':[90, 70], 'games':2, 'seconds':seconds}

def calculate_winprob(data):

	seconds = data['seconds']
	test_data = []
	for i in range(len(seconds)):
		test_data.append([data['awayScores'][i], data['homeScores'][i], seconds[i]])
	td = numpy.array(test_data).astype(float)
	td = td.reshape(len(seconds), -1)
	logisticRegr = joblib.load('model.pkl')
	proba = logisticRegr.predict_proba(td)
	return [prob[1] for prob in proba]
	
@app.route('/')
def default():
	data = get_data()
	proba = calculate_winprob(data)
	data['probs'] = proba
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
		proba = calculate_winprob(data)
		return jsonify({'prob':proba})

class GameStates(Resource):
	
	def get(self):
		data = get_data()
		proba = calculate_winprob(data)
		data['probs'] = proba
		return jsonify(data)
		
api.add_resource(WinProb, '/winprob')
api.add_resource(GameStates, '/games')