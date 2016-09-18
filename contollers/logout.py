from main_handler import Handler


class Logout(Handler):
    def get(self, *args, **kwargs):
        self.response.delete_cookie("user")
        self.session.clear()
        self.redirect("/")