"""OOP implementation"""
from datetime import datetime

class User:
    """user fields"""
    def __init__(self, username, email, password, user_id, admin):
        self.username = username
        self.email = email
        self.password = password
        self.user_id = user_id
        self.admin = admin

class DiaryEntries:
    """docstring for DiaryEntries"""
    def __init__(self, owner, title, entry_id, date):
        self.owner = owner
        self.title = title
        self.entry_id = entry_id
        self.date = datetime.utcnow()