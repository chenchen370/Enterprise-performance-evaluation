from flask import Flask
from flask_cors import CORS  # 如果需要跨域支持


def create_app():
    app = Flask(__name__)

    # 允许跨域请求
    CORS(app)

    # 注册路由
    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app