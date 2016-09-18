import re
from database import *
from tools.hashing import valid_hash


class UserData(object):
    def __init__(self, name, password, password_verify=""):
        self.name = name
        self.password_verify = password_verify
        self.password = password
        self.errors = list()

    def _valid_name(self):
        s_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        return s_re.match(self.name)

    def _valid_password(self):
        s_re = re.compile(r"^.{3,20}$")
        return s_re.match(self.password)

    # def valid_email(self):
    #     s_re = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    #     return s_re.match(self.email)

    def _password_match(self):
        if self.password == self.password_verify:
            return True
        return False

    def is_valid(self):

        if db_model.User.find_by_name(self.name):
            self.errors.append("User already exists")
        if not self.name:
            self.errors.append("Name is missing")
        elif not self._valid_name():
            self.errors.append('Name is invalid')

        if not self.password:
            self.errors.append('Password is missing')
        elif not self._valid_password():
            self.errors.append('Password is invalid')
        elif self.password != self.password_verify:
            self.errors.append('Passwords doesn\'t match')

        if not self.errors:
            return True

    # def id_exist_in_db(self):
    #     user = db_model.User.find_user(self.name)
    #     if user and valid_hash([self.name, self.password], user.password_hash):
    #         return user.key.integer_id()
