from main_handler import Handler
from database.db_model import *


class DeletePage(Handler):
    def get(self, *args, **kwargs):
        link = self.url_lst_part()

        version = self.request.get("v")

        Submissions.delete_entity(link, version)

        self.redirect("/" + link)
