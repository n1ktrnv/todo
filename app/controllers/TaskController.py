from masonite.controllers import Controller
from masonite.exceptions import ModelNotFoundException, AuthorizationException
from masonite.request import Request
from masonite.response import Response
from masonite.views import View
from masoniteorm.query import QueryBuilder

from app.models.Task import Task


class TaskController(Controller):
    def all(self, request: Request, view: View, response: Response):
        user = request.user()

        if not user:
            return response.redirect("/login")

        favorites = Task.where("owner_id", user.id).where(
            "favorite", 1).order_by("done").order_by("created_at", "desc").all()
        non_favorites = Task.where("owner_id", user.id).where(
            "favorite", 0).order_by("done").order_by("created_at", "desc").all()

        done_count = QueryBuilder().table(
            "tasks").where("owner_id", user.id).sum("done").first().get("done")
        count = QueryBuilder().table(
            "tasks").where("owner_id", user.id).count("done").first().get("done")

        return view.render(
            "all",
            {
                "favorites": favorites,
                "non_favorites": non_favorites,
                "done_count": done_count,
                "count": count
            }
        )

    def single(self, request: Request, view: View):
        user = request.user()
        task = Task.find(request.param('id'))

        if not task:
            raise ModelNotFoundException

        if not user or user and task.owner_id != user.id:
            raise AuthorizationException

        return view.render('single', {'task': task})

    def update_favorite_status(self, request: Request, response: Response):
        user = request.user()
        task = Task.find(request.param('id'))

        if not task:
            raise ModelNotFoundException

        if not user or user and task.owner_id != user.id:
            raise AuthorizationException

        task.force_update({"favorite": int(not task.favorite)})
        return response.redirect("/tasks")

    def update_done_status(self, request: Request, response: Response):
        user = request.user()
        task = Task.find(request.param('id'))

        if not task:
            raise ModelNotFoundException

        if not user or user and task.owner_id != user.id:
            raise AuthorizationException

        task.force_update({"done": int(not task.done)})
        return response.redirect("/tasks")

    def add_task(self, request: Request, response: Response):
        user = request.user()

        if not user:
            return response.redirect("/login")

        if not request.input("title"):
            return response.redirect("/tasks/new").with_errors(
                ["Заголовок не может быть пустым"]
            )

        Task.create(
            title=request.input("title"),
            description=request.input("description"),
            done=0,
            favorite=0,
            owner_id=user.id
        )
        return response.redirect("/tasks")

    def update(self, request: Request, response: Response):
        user = request.user()
        task = Task.find(request.param('id'))

        if not task:
            raise ModelNotFoundException

        if not user or user and task.owner_id != user.id:
            raise AuthorizationException

        new_title = request.input("title")
        new_description = request.input("description")
        if new_title == task.title and new_description == task.description:
            return response.redirect("/tasks")

        if not new_title:
            return response.back().with_errors(
                ["Заголовок не может быть пустым."]
            )

        task.force_update({"title": new_title, "description": new_description})

        return response.redirect("/tasks")

    def delete(self, request: Request, response: Response):
        user = request.user()
        task = Task.find(request.param('id'))

        if not task:
            raise ModelNotFoundException

        if not user or user and task.owner_id != user.id:
            raise AuthorizationException

        task.delete()

        return response.redirect("/tasks")

    def add_page(self, request: Request, view: View, response: Response):
        user = request.user()

        if not user:
            return response.redirect("/login")

        return view.render("add")
