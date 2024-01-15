# api/models.py

from mongoengine import Document, StringField, ListField, DictField
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserCollection(Document):
    name          = StringField(required=True)
    email         = StringField(required=True)
    password_hash = StringField()

    @property
    def password(self):
        raise AttributeError('password: write-only field')
    
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    meta = {
        'collection': 'users',
        'indexes': [
            {'fields': ['email'], 'unique': True},
        ]
    }

class UserSearchHistory(Document):
    user_id         = StringField(required=True)
    search_history  = ListField(DictField())

    def add_search_history(self, city, weather_details):
        # Create the search record
        search_record = {
            'timestamp': datetime.now(),
            'city': city,
            'weather_details': weather_details
        }
        self.search_history.append(search_record)
        self.save()
    
    meta = {
        'collection': 'history',
        'indexes': [
            {'fields': ['user_id'], 'unique': True},
        ]
    }