from masonite.routes import Route
from masonite.authentication import Auth

ROUTES = [
    Route.get("/", "WelcomeController@show"),
    Route.get("/tasks", "TaskController@all"),
    Route.get("/tasks/@id:int", "TaskController@single"),
    Route.get(
        "/tasks/update-favorite-status/@id:int",
        "TaskController@update_favorite_status"),
    Route.get(
        "/tasks/update-done-status/@id:int",
        "TaskController@update_done_status"
    ),
    Route.get("/tasks/new", "TaskController@add_page"),
    Route.post("/tasks", "TaskController@add_task"),
    Route.post("/tasks/@id:int", "TaskController@update"),
    Route.get("/tasks/delete/@id:int", "TaskController@delete")
]

ROUTES += Auth.routes()
