from tornado.web import UIModule

LOGGED_IN = 1
LOGGED_OUT = 2


class Navigation(UIModule):

    def render(self, current_user, *args):
        if current_user is not None:
            user_state = LOGGED_IN
        else:
            user_state = LOGGED_OUT

        return self.render_string(
            'navigation.tmpl.html',
            user_state=user_state,
            nav=args)
