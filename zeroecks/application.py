#!/usr/bin/env python

import tempfile
import gnupg
import tornadobase.application
import handlers
import modules


class Application(tornadobase.application.Application):

    def __init__(self):
        self.homedir = tempfile.TemporaryDirectory()
        self.gpg = gnupg.GPG(homedir=self.homedir.name)

        super().__init__()

    def init_settings(self):
        settings = super().init_settings()
        settings['ui_modules'] = modules

        return settings

    def init_handlers(self):

        self.handlers = [
            (r'/', handlers.IndexHandler),
            (r'/trust', handlers.TrustHandler, {'gpg': self.gpg}),
            (r'/assets/', handlers.StaticHandler)]


if __name__ == '__main__':
    app = Application()
    app.start()
