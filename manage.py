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

@manager.command
def runserver():
    socketio = flask_app.extensions.get('socketio')
    if socketio:
        print('>> starting with websockets support')
        socketio.run(flask_app, host='127.0.0.1', port=5000, use_reloader=True, debug=True)
    else:
        print('>> starting just Flask application')
        flask_app.run(host='127.0.0.1', port=5000, use_reloader=True, debug=True)

if __name__ == "__main__":
    manager.run()