from tornado.web import authenticated, HTTPError
from handlers import BaseHandler
from models import Article


class ArticleHandler(BaseHandler):

    def prepare(self):
        self.article = Article(self.dbref)

    async def get(self, id=None):
        article = await self.article.load(id)

        if article is not None:
            self.render('article.tmpl.html',
                        article=article)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')

    @authenticated
    async def post(self):
        '''Create article.
        '''
        article = self.request.body.decode('utf-8')
        article_id = await self.article.create(
            self.current_user, article, True)

        self.write({'id': article_id})

    @authenticated
    async def put(self):
        id = self.get_body_argument('id')
        action = self.get_body_argument('action')

        if id is None:
            raise HTTPError(status_code=404,
                            log_message='Article not found',
                            reason='The article you seek can not be found.')
            return

        if action == 'publish':
            published = self.get_body_argument('published')
            status = published == 'true'
            rowcount = await self.article.publish(
                id, status, self.current_user)

        self.write({'rowcount': rowcount})

    @authenticated
    async def delete(self):
        id = self.get_body_argument('id')
        rowcount = await self.article.delete(id, self.current_user)

        if rowcount is 0:
            raise HTTPError(status_code=404,
                            log_message='Article not found',
                            reason='The article you seek can not be found.')
            return

        self.write({'rowcount': rowcount})


class NewArticleHandler(BaseHandler):

    def prepare(self):
        self.article = Article(self.dbref)

    @authenticated
    async def get(self):
        articles = await self.article.by_author(self.current_user)

        if articles is not None:
            self.render('new_article.tmpl.html',
                        articles=articles)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')
