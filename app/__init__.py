import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để thực hiện chức năng này.'
login_manager.login_message_category = 'warning'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql+psycopg://admin:admin123@localhost:5432/program_course_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.programs import programs_bp
    from app.routes.courses import courses_bp
    from app.routes.program_courses import program_courses_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(programs_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(program_courses_bp)

    return app
