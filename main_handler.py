import webapp2
from jinja2_conf import *
from tools.hashing import valid_user_cookie
from webapp2_extras import sessions


class Handler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.logged_in = True if self.id_from_cookie() else False

    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    @staticmethod
    def render_string(template, **kwargs):
        t = jinja_env.get_template(template)
        return t.render(kwargs)

    def render(self, template, **kwargs):
        logged_in = False
        username = None
        link = self.url_lst_part()

        if self.session:
            logged_in = True
            username = self.session.get("username")

        self.write(self.render_string(
            template,
            logged_in=logged_in,
            username=username,
            link=link,
            **kwargs)
        )

    def id_from_cookie(self):
        user_id_cookie = self.request.cookies.get('user')
        if user_id_cookie and valid_user_cookie(user_id_cookie):
            return user_id_cookie.split('|')[0]

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def url_lst_part(self):
        url = "/".join(self.request.url.split('?')[0].split("/")[3:])  # Split on '?' to cut off get parameters
        if not url:
            return 'main'
        elif url.startswith("_"):  # Ignore _edit and _history
            return "/".join(url.split('/')[1:])
        else:
            return url
