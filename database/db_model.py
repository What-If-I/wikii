from google.appengine.ext import ndb


# User accounts
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    password_hash = ndb.StringProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def find_by_name(cls, username):
        user = cls.query().filter(cls.name == username).get()
        if user:
            return user

    @classmethod
    def name_by_id(cls, user_id):
        user = cls.get_by_id(int(user_id))
        if user:
            return user.name


# Parent for Submissions, used for data consistency
class SubmissionPages(ndb.Model):
    # link = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    created_by = ndb.IntegerProperty(required=True)


# User submissions
class Submissions(ndb.Model):
    title = ndb.TextProperty(required=True)
    content = ndb.TextProperty(required=True)
    created_date = ndb.DateTimeProperty(auto_now_add=True)
    last_modified = ndb.DateTimeProperty(auto_now=True)
    author = ndb.TextProperty(required=True)

    @staticmethod
    def _get_submission_page_key(link):
        submission_page = SubmissionPages.get_by_id(link)
        if submission_page:
            return submission_page.key

    @classmethod
    def all_submissions(cls, link):
        key = cls._get_submission_page_key(link)
        if key:
            return cls.query(ancestor=key).order(-cls.created_date).fetch()

    @classmethod
    def last_submission(cls, link):
        key = cls._get_submission_page_key(link)
        if key:
            return cls.query(ancestor=key).order(-cls.created_date).get()

    @classmethod
    def certain_submission(cls, link, version):
        key = cls._get_submission_page_key(link)
        if key and version:
            return cls.query(ancestor=key).order(cls.created_date).fetch()[int(version)]
        if key and not version:
            return cls.query(ancestor=key).order(-cls.created_date).get()

    @classmethod
    def delete_entity(cls, link, version):
        key = cls._get_submission_page_key(link)
        if key and version:
            entity_key = cls.query(ancestor=key).order(cls.created_date).fetch()[int(version)].key
            entity_key.delete()
