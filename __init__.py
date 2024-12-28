from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extensions import db
from .extensions import migrate


def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tsao0120@127.0.0.1:3306/takemymoney'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:tsao0120@mysql:3306/takemymoney'
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main_routes
        app.register_blueprint(main_routes)

        db.create_all()

    return app
