from app import app
from flask import render_template,request,escape,jsonify
from dataController import dataController
import base64
import urllib2
import json

API_ENDPOINT = 'https://api.twitter.com'
REQUEST_TOKEN_URL =  '%s/oauth2/token' % API_ENDPOINT


@app.route("/",methods=['GET','POST'])
def index():
        """Obtain a bearer token."""
        encoded_bearer_token = base64.b64encode('%s:%s' % ("WdPaWyppZ8ZfuUJOng9g", "zIamt9Liy4vzqpIuVOdPfh3umI6QWBVVNAqj3uAnMk"))
        request = urllib2.Request(REQUEST_TOKEN_URL)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')
        request.add_header('Authorization', 'Basic %s' % encoded_bearer_token)
        request.add_data('grant_type=client_credentials')
        response = urllib2.urlopen(request)
        data = json.load(response)
	app.secret_key=escape(data['access_token'])
        return render_template("index.html")

@app.route("/getStatistics",methods=['POST'])
def getData():
	controller=dataController()
	result=controller.compareTweetCount(request.form['user1'],request.form['user2'],request.form['duration'])
	return jsonify({'data':result,'user1':request.form['user1'],'user2':request.form['user2']})


