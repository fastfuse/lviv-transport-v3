# -*- coding: utf-8 -*-

import jwt
from flask import url_for
from app import db, bcrypt, app
from datetime import datetime, timedelta


class User(db.Model):
    """
    User Model for storing user-related details.
    """
    __tablename__ = "users"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('title', db.Unicode, unique=True)
    password = db.Column('password', db.String(255), nullable=False)
    registered_on = db.Column('registered_on', db.DateTime, nullable=False)
    admin = db.Column('admin', db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode()
        # self.registered_on = datetime.now().replace(microsecond=0) + \
        #     timedelta(hours=3)
        self.registered_on = datetime.now().replace(microsecond=0) + \
            timedelta(hours=3)
        self.admin = admin

    def __repr__(self):
        return '<User object. Username: {}>'.format(self.username)

    def encode_auth_token(self, user_id, user_role):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {'exp': datetime.utcnow() + timedelta(days=1),
                       'iat': datetime.utcnow(),
                       'sub': user_id,
                       'role': user_role}

            return jwt.encode(payload, app.config.get('SECRET_KEY'),
                              algorithm='HS256')

        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token: authentication token
        :return: dict|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)

            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                user_data = {'user': payload['sub'], 'role': payload['role']}
                return user_data

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """ Token Model for storing blacklisted JWT tokens """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token=''):
        self.token = token
        self.blacklisted_on = datetime.now()

    def __repr__(self):
        return '<Token: {}>'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        result = BlacklistToken.query.filter_by(token=str(auth_token)).first()

        if result:
            return True
        else:
            return False
