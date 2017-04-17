#!/usr/bin/env python

import tornadobase.application
import handlers


class Application(tornadobase.application.Application):

    def __init__(self):
        super().__init__()

    def init_handlers(self):

        self.handlers = [
            (r'/', handlers.IndexHandler),
            (r'/assets/', handlers.StaticHandler)]


if __name__ == '__main__':
    app = Application()
    app.start()
