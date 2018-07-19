# app/__init__.py

from flask_api import FlaskAPI
from flask import request, jsonify, abort
import re
from datetime import datetime
from app import models
from app.models import User, DiaryEntries
from functools import wraps


# local import
from instance.config import app_config

users = []
entries = []

def create_app(config_name):
	app = FlaskAPI(__name__, instance_relative_config=True)
	app.config.from_object(app_config["development"])
	app.config.from_pyfile('config.py')

	def login_required(f):
		@wraps(f)
		def wrap(*args, **kwargs):
			credentials = {user.email: user.password for user in users}    
			if email in credentials.keys():
				return f(*args, **kwargs)
			else:
				response = jsonify({'error': 'you need to be logged in'})
				response.status_code = 403
				return response
		return wrap


	@app.route('/api/auth/register/', methods=['POST'])
	def create_user():
		"""api endpoint to create a new user"""
		if request.method == 'POST':
			data = request.get_json()
			email = data.get('email')
			username = data.get('username')
			password = data.get('password')
			admin = data.pop('admin', False)
			regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
			if email == "":
				response = jsonify({'error': 'email field cannot be blank'})
				response.status_code = 400
				return response

			elif not re.match(regex, email):
				response = jsonify({
					'error':'try entering a valid email'
				})
				response.status_code = 403
				return response

			elif username == "":
				response = jsonify({'error' : 'username field cannot be blank'})
				response.status_code = 400
				return response

			elif not re.match("^[a-zA-Z0-9_]*$", username):
				response = jsonify({'error':
									'Username cannot contain special characters'})
				response.status_code = 403
				return response

			elif password == "":
				response = jsonify({'error':'password field has to be filled'})
				response.status_code = 400
				return response
			elif len(password) < 5:#pylint:disable=C1801
				response = jsonify({'error':
									'Password should be more than 5 characters'})
				response.status_code = 403
				return response
			elif len([user for user in users if user.email == email]) > 0:#pylint:disable=C1801
				response = jsonify({'error': 'user already exists'})
				# raise a conflict error
				response.status_code = 409
				return response
			else:
				if len(users) == 0:#pylint:disable=C1801
					user_id = 1
				else:
					user_id = users[-1].user_id + 1
				userslist = {
					'user_id': user_id,
					'username': username,
					'email': email,
					'password': password,
					'admin':admin
					}
				u = User(**userslist)
				users.append(u)
				response = jsonify({'message': 'welcome you now can log in'})
				#users created successfully
				response.status_code = 201
				return response
	@app.route('/api/auth/login/', methods=['POST'])
	def login():
	    """login api endpoint"""
	    data = request.get_json()
	    email = data.get('email')
	    password = data.get('password')
	    if email == "":
	        response = jsonify({'error': 'email field cannot be blank'})
	        response.status_code = 400
	        return response
	    if password == "":
	        response = jsonify({'error': 'password field has to be filled'})
	        response.status_code = 400
	        return response
	    credentials = {user.email: user.password for user in users}
	    if email in credentials.keys():
	        user_password = credentials[email]
	        if user_password == password:
	            response = {
	                'message': 'Login successful'
	            }
	            return jsonify(response), 200
	        response = {'error': 'Invalid password'}
	        return jsonify(response), 401
	    response = {'error': 'User does not exist. Proceed to register'}
	    return jsonify(response), 401

	@app.route('/api/v1/entries/', methods=['POST'])
	def create_diary_entry():
	    """api endpoint to create a new diary entry"""
	    data = request.get_json()
	    owner = data.get('owner')
	    title = data.get('title')
	    if owner == "":
	        response = jsonify({'error': 'provide entry owner'})
	        response.status_code = 400
	        return response

	    if title == "":
	        response = jsonify({'error': 'provide the title for the entry'})
	        response.status_code = 400
	        return response

	    existing = {u.title: u.owner for u in entries}
	    if title in existing.keys():
	        response = jsonify({'error': 'That item exists'})
	        response.status_code = 400
	        return response

	    if len(entries) == 0:#pylint:disable=C1801
	        entry_id = 1
	    else:
	        entry_id = entries[-1].entry_id +1
	    D_entry = {
	        'entry_id': entry_id,
	        'date':datetime.utcnow(),
	        'owner': request.json["owner"],
	        'title': request.json.get('title', "")}
	    de = DiaryEntries(**D_entry)

	    entries.append(de)
	    return jsonify(D_entry, {"message":"created"}), 201
	    
	@app.route('/api/v1/entries/', methods=['GET'])
	def get_entries():
	    """api endpoint to get a list of diary entries"""
	    DiaryList = []
	    for de in entries:
	        DiaryList.append({'date': de.date,
	                          'owner': de.owner,
	                          'entry_id': de.entry_id,
	                          'title': de.title,
	                          'contents':[]
	                         })
	    return jsonify(DiaryList), 200

	return app