from main_handler import Handler
from database.db_model import *


class EditPage(Handler):
    def get(self, *args, **kwargs):
        link = self.url_lst_part()

        version = self.request.get("v")
        if not version:
            version = 0

        submission = Submissions.certain_submission(link, version)

        self.render('edit.html', submission=submission)

    def post(self, *args, **kwargs):
        link = self.url_lst_part()

        user_id = self.session.get("user_id")
        username = self.session.get("username")

        title = self.request.get('title')
        content = self.request.get('user-content')

        submission_page = SubmissionPages.get_by_id(link)

        if not submission_page:
            submission_page = SubmissionPages(
                id=link,
                created_by=int(user_id)
            )
            submission_page.put()

        page_submission = Submissions(
            title=title,
            content=content,
            author=username,
            parent=submission_page.key
        )

        page_submission.put()

        self.redirect("/" + link)
