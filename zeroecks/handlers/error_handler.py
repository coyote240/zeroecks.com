import http.client
from tornadobase.handlers import BaseHandler


class NotFoundHandler(BaseHandler):

    def prepare(self):
        status_code = 404
        reason = http.client.responses[status_code]
        self.set_status(status_code)
        self.render('errors/general.html',
                    status_code=status_code,
                    reason=reason)


class NotAuthorizedHandler(BaseHandler):
    pass
