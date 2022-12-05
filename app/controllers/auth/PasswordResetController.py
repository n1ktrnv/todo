from masonite.controllers import Controller
from masonite.views import View
from masonite.request import Request
from masonite.response import Response
from masonite.authentication import Auth
from masonite.facades import Mail
from app.mailables.ResetPassword import ResetPassword


class PasswordResetController(Controller):
    def show(self, view: View):  # Show password_reset page
        return view.render("auth.password_reset")

    def store(self, auth: Auth, request: Request, response: Response):
        email, reset_token = auth.password_reset(request.input("email"))
        if email:
            Mail.mailable(ResetPassword(token=reset_token).to(email)).send()
            return response.back().with_success(
                [
                    "Письмо отправлено на вашу почту. Пожалуйста, следуйте "
                    "инструкциям из письма."
                ]
            )
        return response.back().with_errors(["Произошла ошибка. Проверьте, верно ли указана почта."])

    def change_password(self, view: View, request: Request):
        return view.render("auth.change_password", {"token": request.param("token")})

    def store_changed_password(self, auth: Auth, request: Request, response: Response):
        password = request.input("password")

        if not password:
            return response.back().with_errors(["Пароль обязателен к заполнению."])

        if not auth.reset_password(password, request.param("token")):
            return response.back().with_errors(["Произошла ошибка. Возможно ваша ссылка недействительна."])

        return response.redirect("/login")
