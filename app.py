import re
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.Charity_Tracker
donations = db.donations
charities = db.charities

app = Flask(__name__)

@app.route('/')
def index():
    '''Return Homepage'''
    return render_template('home.html', charities=charities.find())

@app.route('/charity/new')
def charity_new():
    '''Return page for Creating a New Charity'''
    return render_template('charity_new.html')

@app.route('/charity', methods=['POST'])
def submit_charity():
    '''Submits a New Charity'''
    charity = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'created_at': datetime.datetime.now(),
        'number_of_donations': 0,
        'all_donations': []
    }
    charities.insert_one(charity)
    return redirect(url_for('index'))

@app.route('/charity/<charity_id>/delete', methods=['POST'])
def delete_charity(charity_id):
    """Delete one playlist."""
    charities.delete_one({'_id': ObjectId(charity_id)})
    return redirect(url_for('index'))

if __name__ ==' __main__':
    app.run(debug=True)
