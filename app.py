# encoding=utf8

import logging
from flask import Flask,render_template,request
from config import Config  # 上边的配置文件
from flask_apscheduler.scheduler import APScheduler
from logging.handlers import RotatingFileHandler

# flask-apscheduler内置有日志器，为了让内部的日志器打印的内容输出，我这里做了个配置
# 创建日志记录器，指明日志保存路径，每个日志大小，保存日志文件个数上限
file_log_handler = RotatingFileHandler('logs/runserver.log', maxBytes=1024 * 1024 * 100, backupCount=5)
# 创建日志的记录格式,]，日志等级，记录时间，报错位置，行数，日志信息
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(threadName)s:%(thread)s - %(filename)s - %(funcName)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S %a'
)
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局日志对象添加日志记录器
logger = logging.getLogger("apscheduler")
logger.addHandler(file_log_handler)
logger.setLevel(logging.INFO)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config.from_object(Config)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
# scheduler.add_interval_job(test,seconds=1)
# 配置api权限验证的回调函数
@scheduler.authenticate
def authenticate(auth):
    return auth['username'] == 'guest' and auth['password'] == 'guest'


app.run(host='127.0.0.1', port='7788', debug=True, use_reloader=False)