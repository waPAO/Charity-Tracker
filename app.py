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
        'created_at': datetime.datetime.now()
    }

    charities.insert_one(charity)
    return redirect(url_for('index'))

@app.route('/charity/<charity_id>', methods=['GET'])
def show_charity(charity_id):
    '''Show one Charity'''
    this_charity = charities.find_one({'_id': ObjectId(charity_id)})
    donations_for_charity = donations.find({'charity': ObjectId(charity_id)})
    return render_template('show_charity.html',  charity=this_charity, donations=donations_for_charity)

@app.route('/charity/<charity_id>/delete', methods=['POST'])
def delete_charity(charity_id):
    """Delete one playlist."""
    charities.delete_one({'_id': ObjectId(charity_id)})
    return redirect(url_for('index'))

@app.route('/donation/create', methods=['POST'])
def create_donation():
    donation = {
        'name': request.form.get('name'),
        'amount': request.form.get('amount'),
        'charity': request.form.get('charity'),
        'created_at': datetime.datetime.now()
    }

    donations.insert_one(donation)
    return redirect(url_for('show_charity', charity_id=request.form.get('charity')))

if __name__ ==' __main__':
    app.run(debug=True)
