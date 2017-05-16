from handlers import BaseHandler


class IndexHandler(BaseHandler):

    async def get(self):

        with self.dbref.cursor() as cursor:
            cursor.execute('''
            SELECT id, author, content
            FROM site.articles
            ''')

            articles = cursor.fetchall()

        self.render('index.tmpl.html',
                    articles=articles)
