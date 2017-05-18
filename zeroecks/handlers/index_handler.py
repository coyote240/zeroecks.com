from handlers import BaseHandler


class IndexHandler(BaseHandler):

    async def get(self):

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            SELECT  id, author, content, date_created
            FROM    site.articles
            WHERE   published = TRUE
            ORDER BY date_created DESC
            ''')

            articles = cursor.fetchall()

        self.render('index.tmpl.html',
                    articles=articles)
