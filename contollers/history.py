from main_handler import Handler
from database.db_model import *
from datetime import datetime


class HistoryPage(Handler):
    def get(self, *args, **kwargs):
        link = self.url_lst_part()
        submissions = Submissions.all_submissions(link)

        if submissions:
            self.render('history.html', submissions=submissions)
        else:
            self.redirect('/_edit/' + link)
