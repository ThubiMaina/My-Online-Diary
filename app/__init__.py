# app/__init__.py
import re
from datetime import datetime
from flask_api import FlaskAPI
from flask import request, jsonify, abort
from app import models
from app.models import *
from app.auth import auth_token

# local import
from instance.config import app_config

users = []
entries = []
contents = []

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config["development"])
    app.config.from_pyfile('config.py')

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
            encrypted_password = credentials[email]
            if Bcrypt().check_password_hash(encrypted_password, password):
                access_token = User.generate_token(email)
                if access_token:
                    response = {
                        'message': 'Login successful',
                        'access_token': access_token
                    }
                    return jsonify(response), 200
            response = {'error': 'Invalid email or password'}
            return jsonify(response), 401       
        response = {'error': 'User does not exist. Proceed to register'}
        return jsonify(response), 401


    @app.route('/api/v1/users/', methods=['GET'])
    @auth_token
    def get_all_users(current_user_email):
        """api endpoint for getting all users"""
        userlist = []
        for user in users:
            userlist.append(
                {'user_id': user.user_id, 'username': user.username,
                 'admin': user.admin, 'email': user.email})
        if len(userlist) == 0:#pylint:disable=C1801
            response = jsonify({"error":"there are no users registered "})
            response.status_code = 404
            return response
        return jsonify(userlist), 200

    @app.route('/api/v1/entries/', methods=['POST'])
    @auth_token
    def create_diary_entry(current_user_email):
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
        response = jsonify({"message": "entry created"})
        response.status_code = 201
        return response

    @app.route('/api/v1/entries/', methods=['GET'])
    @auth_token
    def get_entries(current_user_email):
        """api endpoint to get a list of diary entries"""
        DiaryList = []
        for de in entries:
            DiaryList.append({'date': de.date,
                              'owner': de.owner,
                              'entry_id': de.entry_id,
                              'title': de.title
                             })
        return jsonify(DiaryList), 200

    @app.route('/api/v1/entries/<int:entry_id>/', methods=['GET'])
    @auth_token
    def get_single_entry(entry_id, current_user_email):
        """api endpoint to get a single diary entry"""
        entry = [entry for entry in entries if entry.entry_id == entry_id]
        if len(entry) == 0:#pylint:disable=C1801
            response = jsonify({'error': 'item not found'})
            response.status_code = 404
            return response
        de = entry[0]
        return jsonify({'date':de.date,
                        'owner': de.owner,
                        'entry_id': de.entry_id,
                        'title': de.title,
                       }), 200
    @app.route('/api/v1/entries/<int:entry_id>/', methods=['PUT'])
    @auth_token
    def update_diary_entry(entry_id, current_user_email):
        """api endpoint to edit a diary entry"""
        data = request.get_json()
        title = data.get('title')
        entry = [entry for entry in entries if entry.entry_id == entry_id]
        if len(entry) == 0:#pylint:disable=C1801
            response = jsonify({'error': 'item not found'})
            response.status_code = 404
            return response
        if not request.json:
            abort(400)
        owner = request.json["owner"]
        de = entry[0]

        if de.owner != owner:
            response = jsonify({'error': 'only edit the entry name'})
            response.status_code = 400
            return response

        existing = {u.title: u.owner for u in entries}
        if title in existing.keys():
            response = jsonify({'error': 'no change detected'})
            response.status_code = 400
            return response

        if 'title' in request.json:
            de.title = request.json["title"]
        return jsonify({'date':de.date,
                        'owner': de.owner,
                        'entry_id': de.entry_id,
                        'title': de.title
                       }), 201
    @app.route('/api/v1/entries/<int:entry_id>/', methods=['DELETE'])
    @auth_token
    def delete_entry(entry_id, current_user_email):
        """api endpoint to delete a single entry"""
        entry = [entry for entry in entries if entry.entry_id == entry_id]
        if len(entry) == 0:#pylint:disable=C1801
            response = jsonify({'error': 'item not found'})
            response.status_code = 404
            return response
        de = entry[0]
        entries.remove(de)
        return jsonify({'result': 'item deleted'}), 202

    @app.route('/api/v1/entries/<int:entry_id>/contents/', methods=['POST'])
    @auth_token
    def create_content(entry_id, current_user_email):
        data = request.get_json()
        content = data.get('contents')
        if contents == '':
            abort(400)
        if entry_id =='':
            abort(400)
        if len(contents) == 0:#pylint:disable=C1801
            content_id = 1
        else:
            content_id = contents[-1].content_id +1
        content = {
            'content_id': content_id,
            'diary_id':entry_id,
            'date':datetime.utcnow(),
            'content': request.json.get('contents')
            }

        cl = Content(**content)

        contents.append(cl)
        response = jsonify({"message": "content added"})
        response.status_code = 201
        return response

    @app.route('/api/v1/entries/<int:entry_id>/contents/', methods=['GET'])
    @auth_token
    def get_contents(entry_id, current_user_email):
        """api endpoint to get a list of the contents to a  diary entry"""
        contentlist = []
        for list_content in contents:
            contentlist.append({'date': list_content.date,
                              "content_id":list_content.content_id,
                              'diary_id': list_content.diary_id,
                              "contents":list_content.content
                             })
        return jsonify(contentlist), 200

    return app