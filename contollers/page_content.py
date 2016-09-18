from main_handler import Handler
from database.db_model import *


class PageContent(Handler):
    def get(self, *args, **kwargs):
        link = self.url_lst_part()

        version = self.request.get("v")

        submission = Submissions.certain_submission(link, version)

        if submission:
            self.render('content.html', submission=submission)
        else:
            self.redirect('/_edit/' + link)
