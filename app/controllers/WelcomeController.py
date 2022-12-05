"""A WelcomeController Module."""
from masonite.authentication import Auth
from masonite.controllers import Controller
from masonite.response import Response


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, auth: Auth, response: Response):
        if auth.user():
            return response.redirect('/tasks')
        return response.redirect('/login')
