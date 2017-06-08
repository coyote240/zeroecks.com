from tornado import gen
from handlers import BaseHandler
from models import Article


class IndexHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        articles = yield Article(self.dbref).all()

        self.render('index.tmpl.html',
                    articles=articles)
