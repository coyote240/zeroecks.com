import uuid
import bleach
import markdown
from collections import namedtuple
from tornado import gen


class Article(object):

    def __init__(self, connection):
        self.connection = connection
        self.allowed_tags = bleach.sanitizer.ALLOWED_TAGS + [
                u'h1', u'h2', u'p']

    @gen.coroutine
    def all(self):
        Record = namedtuple('Record', 'id, author, content, date_created')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  alt_id, author, content, date_created
            FROM    site.articles
            WHERE   published = TRUE
            ORDER BY date_created DESC
            ''')

            articles = map(Record._make, cursor.fetchall())

        return articles

    @gen.coroutine
    def load(self, alt_id):
        Record = namedtuple('Record', '''
            id, author, content, raw_input, date_created
        ''')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  alt_id,
                    author,
                    content,
                    raw_input,
                    date_created
            FROM    site.articles
            WHERE   alt_id = %s
            ''', (alt_id,))
            res = cursor.fetchone()

        if res is None:
            return None
        return Record._make(res)

    @gen.coroutine
    def by_author(self, author):
        Record = namedtuple(
            'Record',
            'id, content, date_created, date_updated, published')

        with self.connection.cursor() as cursor:
            cursor.execute('''
            SELECT  alt_id,
                    content,
                    date_created,
                    date_updated,
                    published
            FROM    site.articles
            WHERE   author = %s
            ORDER BY date_updated DESC
            ''', (author, ))

            articles = map(Record._make, cursor.fetchall())

        return articles

    @gen.coroutine
    def create(self, author, article, published=False):
        alt_id = uuid.uuid4().hex
        cleansed_article = self.sanitize(article)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO site.articles
                (alt_id, author, content, raw_input, published)
            values (%s, %s, %s, %s, %s)
            RETURNING alt_id
            ''', (alt_id, author, cleansed_article, article, published))
            (article_id,) = cursor.fetchone()

        return article_id

    @gen.coroutine
    def update(self, alt_id, article, author, published=False):
        cleansed_article = self.sanitize(article)

        with self.connection.cursor() as cursor:
            cursor.execute('''
            UPDATE  site.articles
            SET     date_updated = now(),
                    content = %s,
                    raw_input = %s,
                    published = %s
            WHERE   alt_id = %s
            AND     author = %s
            RETURNING alt_id
            ''', (cleansed_article, article, published, alt_id, author))
            (article_id,) = cursor.fetchone()

        return article_id

    @gen.coroutine
    def delete(self, alt_id, author):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            DELETE FROM site.articles
            WHERE   alt_id = %s
            AND     author = %s
            ''', (alt_id, author))
            rowcount = cursor.rowcount

        return rowcount

    @gen.coroutine
    def publish(self, alt_id, published, author):
        with self.connection.cursor() as cursor:
            cursor.execute('''
            UPDATE  site.articles
            SET     date_updated = now(),
                    published = %s
            WHERE   alt_id = %s
            AND     author = %s
            ''', (published, alt_id, author))
            rowcount = cursor.rowcount

        return rowcount

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
