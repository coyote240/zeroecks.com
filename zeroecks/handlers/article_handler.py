from tornado.web import authenticated
from handlers import BaseHandler


class ArticleHandler(BaseHandler):

    def get(self, id=None):
        self.render('article.tmpl.html', article=id)


class NewArticleHandler(BaseHandler):

    @authenticated
    def get(self, id=None):
        self.render('new_article.tmpl.html')

    @authenticated
    async def post(self):
        pass

    @authenticated
    async def put(self):
        pass
