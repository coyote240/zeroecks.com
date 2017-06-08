from tornado.web import authenticated, HTTPError
from tornado import gen
from . import BaseHandler
from ..models import Article


class ArticleHandler(BaseHandler):

    def prepare(self):
        self.article = Article(self.dbref)

    @gen.coroutine
    def get(self, id=None):
        article = yield self.article.load(id)

        if article is not None:
            self.render('article.tmpl.html',
                        article=article)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')

    @authenticated
    @gen.coroutine
    def post(self):
        '''Create article.
        '''
        article = self.request.body.decode('utf-8')
        article_id = yield self.article.create(
            self.current_user, article)

        self.write({'id': article_id})

    @authenticated
    @gen.coroutine
    def put(self):
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
            rowcount = yield self.article.publish(
                id, status, self.current_user)

        self.write({'rowcount': rowcount})

    @authenticated
    @gen.coroutine
    def delete(self):
        id = self.get_body_argument('id')
        rowcount = yield self.article.delete(id, self.current_user)

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
    @gen.coroutine
    def get(self):
        articles = yield self.article.by_author(self.current_user)

        if articles is not None:
            self.render('new_article.tmpl.html',
                        articles=articles)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')


class EditArticleHandler(BaseHandler):

    def prepare(self):
        self.article = Article(self.dbref)

    @authenticated
    @gen.coroutine
    def get(self, id=None):

        if id is None:
            raise HTTPError(status_code=400,
                            log_message='Bad Request',
                            reason='Article ID required')

        article = yield self.article.load(id)
        if article is not None:
            self.render('edit_article.tmpl.html',
                        article=article)
            return

        raise HTTPError(status_code=404,
                        log_message='Article not found',
                        reason='The article you seek can not be found.')

    @authenticated
    @gen.coroutine
    def post(self, id):
        article = self.get_body_argument('article')

        if id is None:
            raise HTTPError(status_code=400,
                            log_message='Bad Request',
                            reason='Article ID Required')
            return

        rowcount = yield self.article.update(id, article, self.current_user)

        if rowcount is 0:
            raise HTTPError(status_code=404,
                            log_message='Article not found',
                            reason='The article you seek can not be found.')
            return

        self.redirect(self.reverse_url('Article', id))
