from tornado.web import authenticated, HTTPError
from handlers import BaseHandler
from models import Article


class ArticleHandler(BaseHandler):

    async def get(self, id=None):
        article = await Article(self.dbref).load(id)

        if article is not None:
            self.render('article.tmpl.html',
                        article=article)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')

    @authenticated
    async def delete(self, id=None):
        if id is not None:
            article_id = await Article(self.dbref).delete(id)
            self.write({'id': article_id})
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')


class NewArticleHandler(BaseHandler):

    @authenticated
    async def get(self):
        articles = await Article(self.dbref).by_author(self.current_user)

        if articles is not None:
            self.render('new_article.tmpl.html',
                        articles=articles)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')

    @authenticated
    async def post(self):
        '''Create article.
        '''
        article = self.request.body.decode('utf-8')
        article_id = await Article(self.dbref).create(
            self.current_user, article, True)

        self.write({'id': article_id})

    @authenticated
    async def put(self, id=None):
        '''Update article.
        Update stored article with given id, as owned by the currently
        logged in user.
        '''
        article = self.request.body.decode('utf-8')
        cleansed_article = self.sanitize_article(article)

        if id is not None:
            updated_id = await Article(self.dbref).update(
                    id, cleansed_article, self.current_user)

            self.write({'id': updated_id})
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')
