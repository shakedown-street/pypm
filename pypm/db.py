import datetime

from peewee import *

db = SqliteDatabase("peeweepm.db")


class BaseModel(Model):
    class Meta:
        database = db


class Project(BaseModel):
    name = CharField(max_length=256)
    slug = CharField(max_length=256, unique=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(
        default=datetime.datetime.now, constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )
    status = CharField(max_length=32, default="active")


class Task(BaseModel):
    project = ForeignKeyField(Project, backref="tasks")
    title = CharField(max_length=256)
    body = TextField()
    status = CharField(max_length=32)
    priority = CharField(max_length=32)
    due_date = DateTimeField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(
        default=datetime.datetime.now, constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )


def init_db():
    db.connect()
    db.create_tables([Project, Task], safe=True)
    db.close()
