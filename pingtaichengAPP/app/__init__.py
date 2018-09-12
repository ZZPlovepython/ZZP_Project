#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
import sys

bootstrap = Bootstrap()
db = SQLAlchemy()


def creat_app(config_name):
    #app = Flask(__name__)
    app = None  
    if getattr(sys, 'frozen', False):  
        template_folder = os.path.join(sys.executable, '..', 'templates')  
        static_folder = os.path.join(sys.executable, '..', 'static')  
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)  
    else:  
        app = Flask(__name__)#打包的工作
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    # 附加路由和自定义错误页面,蓝本导入示例
    from .main import main as main_blueprint
    from .enginer import engineer as engineer_blueprint
    from .report import report as report_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(engineer_blueprint, url_prefix='/engineer')
    app.register_blueprint(report_blueprint, url_prefix='/report')
    return app
