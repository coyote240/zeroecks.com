import markdown
import bleach
from tornado.web import authenticated, HTTPError
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
            AND     published = TRUE
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
        '''Create article.
        '''
        article = self.request.body.decode('utf-8')
        cleansed_article = self.sanitize_article(article)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            INSERT INTO site.articles (author, content)
            values (%s, %s)
            RETURNING id
            ''', (self.current_user, cleansed_article))

            next_id = cursor.fetchone()[0]

        self.write({'id': next_id})

    @authenticated
    async def put(self, id=None):
        '''Update article.
        Update stored article with given id, as owned by the currently
        logged in user.
        '''
        if id is None:
            raise HTTPError(status_code=404,
                            log_message='Article not found',
                            reason='The article you seek can not be found.')

        article = self.request.body.decode('utf-8')
        cleansed_article = self.sanitize_article(article)

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            UPDATE  site.articles
            SET     date_modified = now(),
                    content = %s
            WHERE   id = %s
            AND     author = %s
            ''', (cleansed_article, id, self.current_user))

        self.write({'id': id})

    @authenticated
    async def delete(self, id=None):
        '''Delete article.
        Delete stored article with given id, as owned by the currently
        logged in user.
        '''
        if id is None:
            raise HTTPError(status_code=404,
                            log_message='Article not found',
                            reason='The article you seek can not be found.')

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            DELETE  FROM site.articles
            WHERE   id = %s
            AND     author = %s
            ''', (id, self.current_user))

        self.write({'id': id})

    def sanitize_article(self, article):
        '''Sanitize user-submitted article.
        Given a raw markdown string, convert it to HTML and sanitize it.
        '''
        formatted_article = markdown.markdown(article)
        cleansed_article = bleach.clean(formatted_article,
                                        tags=self.allowed_tags,
                                        protocols=['http', 'https'],
                                        strip=True)
        return bleach.linkify(cleansed_article)
