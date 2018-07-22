"""OOP implementation"""
from flask_bcrypt import Bcrypt
from flask import Flask
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta

class User:
    """user fields"""
    def __init__(self, username, email, password, user_id, admin):
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.user_id = user_id
        self.admin = admin

    @staticmethod
    def generate_token(email):
        try:
            payload = {
            'iss': "mydiary",
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'sub': email
            }
            jwt_string = jwt.encode(payload,
             'secret', algorithm='HS256')
            return jwt_string.decode("utf-8")
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            payload = jwt.decode(token, 'secret')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return {"error": "Expired token. Please login to get a new token"}
        except jwt.InvalidTokenError:
            return {"error":"Invalid token. Please register or login"}

class DiaryEntries:
    """docstring for DiaryEntries"""
    def __init__(self, owner, title, entry_id, date):
        self.owner = owner
        self.title = title
        self.entry_id = entry_id
        self.date = datetime.utcnow()

class Content:
    def __init__(self, content_id, diary_id, content, date ):
        self.content_id = content_id
        self.diary_id = diary_id
        self.content = content
        self.date = datetime.utcnow()


