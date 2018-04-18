from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from lxml import html
import requests
from scraper import scrape, time_to_seconds
app = Flask(__name__)
api = Api(app)

@app.route('/')
def default():
	data = scrape()
	seconds = time_to_seconds(data['clock'])
	data['clock'] = seconds
	return render_template('index.html', data=data)