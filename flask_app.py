from flask import Flask
from flask_login import LoginManager

from celery import Celery

from models import User, db
import os

app = Flask(__name__)

app.config['DB'] = db
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['UPLOAD_FOLDER'] = os.path.join('static','uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.config['DB'].init_app(app)
app.config['DB'].create_all(app=app)

# app.config.update(CELERY_CONFIG={
#     'broker_url': 'pyamqp://','result_backend': 'rpc://'
#     # 'broker_url': 'redis://localhost:6379',
#     # 'result_backend': 'redis://localhost:6379',
# })

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from auth.routes import auth as auth_blueprint
from app.mnist import main as main_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)

# def make_celery(app):
#     celery = Celery(app.import_name)
#     celery.conf.update(app.config["CELERY_CONFIG"])

#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery.Task = ContextTask
#     return celery

# celery_app = make_celery(app)


if __name__ == '__main__':
    app.run()