from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth


class RegisterController(Controller):
    def show(self, auth: Auth, view: View, response: Response):  # Show register page
        if auth.user():
            return response.redirect("/tasks")
        return view.render("auth.register")

    def store(
        self, auth: Auth, request: Request, response: Response
    ):
        email = request.input("email")
        password = request.input("password")

        errors = []
        if not email:
            errors.append("Почта обязательная к заполнению.")
        if not password:
            errors.append("Пароль обязателен к заполнению.")

        if errors:
            return response.back().with_errors(errors)

        user = auth.register({
            "name": "",
            "email": email,
            "password": password
        })

        if not user:
            return response.redirect("/register").with_errors([
                "Произошла ошибка. Возможно пользователь с таким email уже зарегистрирован."
            ])

        return response.redirect("/tasks")
