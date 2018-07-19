# app/__init__.py

from flask_api import FlaskAPI
from flask import request, jsonify, abort
import re
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
	return app