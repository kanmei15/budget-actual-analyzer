from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

import os

load_dotenv()

db = SQLAlchemy()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)

login_manager = LoginManager()

# Swagger UI を /swagger に設定
restx_api = Api(
    title='Tools API',
    version='1.0',
    description='Tools API with Swagger UI',
    doc='/swagger',
    prefix='/api'
)

def create_app(config_name='DevelopmentConfig'):
    app = Flask(__name__)

    config_name = os.getenv('FLASK_CONFIG', 'DevelopmentConfig')

    config_map = {
        'DevelopmentConfig': DevelopmentConfig,
        'ProductionConfig': ProductionConfig,
        'TestingConfig': TestingConfig
    }
    app.config.from_object(config_map[config_name])

    JWTManager(app)

    Talisman(app, content_security_policy=app.config.get('CONTENT_SECURITY_POLICY'))

    db.init_app(app)
    restx_api.init_app(app)
    limiter.init_app(app)

    # app/api/__init__.py から namespaces をインポート
    from app.api import namespaces
    # Namespaceをアプリケーションに登録
    for ns in namespaces:
        restx_api.add_namespace(ns)  # apiオブジェクトにnamespaceを追加

    # Blueprintのインポート
    from app.views.auth import auth_bp  # auth_bp をインポート
    app.register_blueprint(auth_bp, url_prefix='/auth')  # Blueprintをアプリに登録

    from app.views.web import web_bp  # web_bp をインポート
    app.register_blueprint(web_bp, url_prefix='/web')  # Blueprintをアプリに登録

    # Flask-Loginの設定
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 

    # ユーザーの読み込み関数を定義
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    return app
