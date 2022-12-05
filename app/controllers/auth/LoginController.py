from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class LoginController(Controller):
    def show(self, auth: Auth, view: View, response: Response):
        if auth.user():
            return response.redirect("/tasks")
        return view.render("auth.login")

    def store(self, request: Request, auth: Auth, response: Response):
        username = request.input("username")
        password = request.input("password")

        errors = []
        if not username:
            errors.append("Почта обязательна к заполнению.")
        if not password:
            errors.append("Пароль обязателен к заполнению.")
        if errors:
            return response.back().with_errors(errors)

        login = auth.attempt(
            request.input("username"), request.input("password"))

        if login:
            return response.redirect("/tasks")

        return response.redirect(name="login").with_errors(
            ["Вы ввели неверный логин или пароль."]
        )

    def logout(self, auth: Auth, response: Response):
        auth.logout()
        return response.redirect(name="login")
