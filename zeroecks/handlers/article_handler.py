import markdown
import bleach
from tornado.web import authenticated
from handlers import BaseHandler


class ArticleHandler(BaseHandler):

    async def get(self, id=None):

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            SELECT  author,
                    content,
                    date_created
            FROM    site.articles
            WHERE   id = %s
            ''', (id, ))

            (author, content, date_created) = cursor.fetchone()

        self.render('article.tmpl.html',
                    id=id,
                    author=author,
                    date_created=date_created,
                    content=content)


class NewArticleHandler(BaseHandler):

    def initialize(self):
        super().initialize()

        self.allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
                u'h1', u'h2', u'p']

    @authenticated
    def get(self, id=None):
        self.render('new_article.tmpl.html')

    @authenticated
    async def post(self):
        article = self.request.body.decode('utf-8')
        formatted_article = markdown.markdown(article)
        cleansed_article = bleach.clean(formatted_article,
                                        tags=self.allowed_tags,
                                        protocols=['http', 'https'],
                                        strip=True)
        cleansed_article = bleach.linkify(cleansed_article)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            INSERT INTO site.articles (author, content)
            values (%s, %s)
            RETURNING id
            ''', (self.current_user, cleansed_article))

            next_id = cursor.fetchone()[0]

        self.write({
            'id': next_id
        })

    @authenticated
    async def put(self):
        pass
