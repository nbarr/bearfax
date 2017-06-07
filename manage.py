# manage.py

from flask_script import Manager

from application import flask_app

manager = Manager(flask_app)

@manager.command
def create_db():
    "Creates database tables from sqlalchemy models"
    from application.models import User, Role, Task, Base
    from application.database.engine import database_engine

    Base.metadata.create_all(database_engine)

if __name__ == "__main__":
    manager.run()