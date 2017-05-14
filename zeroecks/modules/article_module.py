from tornado.web import UIModule


class Article(UIModule):

    def render(self, article):
        id, author, content = article

        return self.render_string('article.tmpl.html',
                                  id=id,
                                  content=content)
