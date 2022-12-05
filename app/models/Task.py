""" Task Model """

from masoniteorm.models import Model
from masoniteorm.relationships import belongs_to


class Task(Model):
    __table__ = "tasks"
    __fillable__ = ["title", "description", "done", "favorite", "owner_id"]

