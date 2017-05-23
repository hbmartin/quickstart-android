#!/usr/bin/env python3

"""Authed Firebase"""

__author__ = "H. Martin"
__version__ = "0.1.0"

import json
from pyrebase.pyrebase import Firebase, Database


class Fb(Firebase):
    def __init__(self, google_services, email, password):
        with open(google_services, encoding='utf-8') as data_file:
            firebase_config = json.loads(data_file.read())
        pyrebase_config = {
            "apiKey": firebase_config["client"][0]["api_key"][0]["current_key"],
            "authDomain": firebase_config["project_info"]["storage_bucket"],
            "databaseURL": firebase_config["project_info"]["firebase_url"],
            "storageBucket": firebase_config["project_info"]["storage_bucket"]
        }
        super().__init__(pyrebase_config)
        self.user = self.auth().sign_in_with_email_and_password(email, password)

    def database(self):
        return Adb(self.credentials, self.api_key, self.database_url, self.requests, self.user)

class Adb(Database):
    def __init__(self, credentials, api_key, database_url, requests, usr):
        super().__init__(credentials, api_key, database_url, requests)
        self.user = usr

    def get(self, token=None, *args, **kwargs):
        if token is None and self.user is not None:
            token = self.user['idToken']
        super().get(token, *args, **kwargs) # wtf - apparently this call failed without giving it a first try?
        return super().get(token, *args, **kwargs)

    def push(self, data, token=None, *args, **kwargs):
        if token is None and self.user is not None:
            token = self.user['idToken']
        return super().push(data, token, *args, **kwargs)

    def set(self, data, token=None, *args, **kwargs):
        if token is None and self.user is not None:
            token = self.user['idToken']
        return super().set(data, token, *args, **kwargs)

    def update(self, data, token=None, *args, **kwargs):
        if token is None and self.user is not None:
            token = self.user['idToken']
        return super().update(data, token, *args, **kwargs)

    def remove(self, *args, **kwargs):
        if token is None and self.user is not None:
            token = self.user['idToken']
        return super().remove(*args, **kwargs)

    def check_token(self, database_url, path, token):
        if token is None and self.user is not None:
            token = self.user['idToken']
        return super().check_token(database_url, path, token)