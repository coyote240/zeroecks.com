import bleach
import markdown
from collections import namedtuple


class Article(object):

    def __init__(self, connection):
        self.connection = connection
        self.allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
                u'h1', u'h2', u'p']

    async def all(self):
        Record = namedtuple('Record', 'id, author, content, date_created')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  id, author, content, date_created
            FROM    site.articles
            WHERE   published = TRUE
            ORDER BY date_created DESC
            ''')

            articles = map(Record._make, cursor.fetchall())

        return articles

    async def load(self, id):
        Record = namedtuple('Record', 'id, author, content, date_created')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  id, author, content, date_created
            FROM    site.articles
            WHERE   id = %s
            AND     published = TRUE
            ''', (id, ))
            res = cursor.fetchone()

        if res is None:
            return None
        return Record._make(res)

    async def by_author(self, author, published=True):
        Record = namedtuple(
            'Record',
            'id, content, date_created, date_updated, published')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  id,
                    content,
                    date_created,
                    date_updated,
                    published
            FROM    site.articles
            WHERE   author = %s
            AND     published = %s
            ORDER BY date_updated DESC
            ''', (author, published))

            articles = map(Record._make, cursor.fetchall())

        return articles

    async def create(self, author, article, published=False):
        cleansed_article = self.sanitize(article)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO site.articles (author, content, published)
            values (%s, %s, %s)
            RETURNING id
            ''', (author, cleansed_article, published))
            (article_id,) = cursor.fetchone()

        return article_id

    def update(self, id, article, author):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            UPDATE  site.articles
            SET     date_modified = now(),
                    content = %s
            WHERE   id = %s
            AND     author = %s
            ''', (article, id, author))

        return id

    async def delete(self, id, author):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            DELETE FROM site.articles
            WHERE   id = %s
            AND     author = %s
            ''', (id, author))

        return id

    def publish(self):
        pass

    def sanitize(self, article):
        '''Sanitize user-submitted article.
        Given a raw markdown string, convert it to HTML and sanitize it.
        '''
        formatted_article = markdown.markdown(article)
        cleansed_article = bleach.clean(formatted_article,
                                        tags=self.allowed_tags,
                                        protocols=['http', 'https'],
                                        strip=True)
        return bleach.linkify(cleansed_article)
