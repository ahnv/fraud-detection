"""
Routes and views for the flask application.
"""

from api import app
from api.apiwrapper import apiwrapper
from datetime import datetime
from flask import render_template, request, jsonify, make_response
import pandas as pd

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('index.html')

@app.route('/summary')
def summary():
    aw = apiwrapper()
    return aw.generateGraph()

@app.route('/score', methods=['GET','POST'])
def score():
    content = request.get_json(force=True)
    aw = apiwrapper()
    p = aw.postTransactionDetails(content)
    return jsonify(p)



@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

