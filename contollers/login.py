from main_handler import Handler
from models.user import *
from tools import hashing


class LoginPage(Handler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        user = UserData(
            name=self.request.get("username"),
            password=self.request.get("password"),
        )

        db_user = db_model.User.find_by_name(username=user.name)

        if db_user and valid_hash([user.name, user.password], db_user.password_hash):
            user_id = db_user.key.integer_id()
            cookie = hashing.make_hash(str(user_id), return_value=user_id, secret=True)

            remember = self.request.get("remember-me")
            self.response.set_cookie("user", cookie, max_age=10**7 if remember else None)
            self.session['username'] = user.name
            self.session['user_id'] = user_id

            self.redirect("/")
        else:
            self.render("login.html", username_input=user.name, error="Invalid login or password")
