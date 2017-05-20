from handlers import BaseHandler
from models import Article


class IndexHandler(BaseHandler):

    async def get(self):
        articles = await Article(self.dbref).all()

        self.render('index.tmpl.html',
                    articles=articles)
