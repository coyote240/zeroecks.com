from tornado.web import authenticated
from handlers import BaseHandler


class ArticleHandler(BaseHandler):

    async def get(self, id=None):

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            SELECT  author, content
            FROM    site.articles
            WHERE   id = %s
            ''', (id, ))

            (author, content) = cursor.fetchone()

        self.render('article.tmpl.html',
                    id=id,
                    content=content)


class NewArticleHandler(BaseHandler):

    @authenticated
    def get(self, id=None):
        self.render('new_article.tmpl.html')

    @authenticated
    async def post(self):
        self.warn(self.request.files)
        article = str(self.request.body)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            INSERT INTO site.articles (author, content)
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
