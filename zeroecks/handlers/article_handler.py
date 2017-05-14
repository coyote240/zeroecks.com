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
        article = self.request.body

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            INSERT INTO articles.articles (author, content)
            values (%s, %s)
            RETURNING id
            ''', (self.current_user, article))

            next_id = cursor.fetchone()[0]

        self.write({
            'id': next_id
        })

    @authenticated
    async def put(self):
        pass
