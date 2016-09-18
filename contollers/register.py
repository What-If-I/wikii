from main_handler import Handler
from database import db_model
from models.user import UserData
from tools import hashing


class RegisterPage(Handler):
    def get(self, *args, **kwargs):
        self.render('register.html')

    def post(self, *args, **kwargs):
        user = UserData(
            name=self.request.get("username"),
            password=self.request.get("password"),
            password_verify=self.request.get("password-verify")
        )

        if user.is_valid():
            new_user = db_model.User(name=user.name,
                                     password_hash=hashing.make_hash([user.name, user.password])
                                     )
            new_user.put()

            user_id = str(new_user.key.integer_id())
            cookie = hashing.make_hash(user_id, return_value=user_id, secret=True)

            self.response.set_cookie("user", cookie)
            self.session['username'] = user.name
            self.session['user_id'] = user_id

            self.redirect("/")

        else:
            self.render("register.html", username_input=user.name, errors=user.errors)
