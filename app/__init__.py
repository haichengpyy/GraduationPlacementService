from flask import Flask
from app.controller import  uicer,  offer, alumni,KnowledgePoint


# 定义注册蓝图方法
def register_blueprints(app):

    app.register_blueprint(uicer.uicerBP, url_prefix='/uicer')

    app.register_blueprint(offer.offerBP, url_prefix='/offer')
    app.register_blueprint(alumni.alumniBP, url_prefix='/alumni')
    app.register_blueprint(KnowledgePoint.knowledgeBP, url_prefix='/knowledge')

# 注册插件(数据库关联)
def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    # create_all要放到app上下文环境中使用
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__)
    # app.config.from_object('app.config.setting') # 基本配置(setting.py) 
    app.config.from_object('app.config.secure')  # 重要参数配置(secure.py)
    # 注册蓝图与app对象相关联
    register_blueprints(app)
    # 注册插件(数据库)与app对象相关联
    register_plugin(app)
    # 一定要记得返回app
    return app
