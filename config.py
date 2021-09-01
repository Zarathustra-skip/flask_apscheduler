from apscheduler.jobstores.redis import RedisJobStore
from flask_apscheduler.auth import HTTPBasicAuth

class Config(object):
    # �洢��ʱ����Ĭ���Ǵ洢���ڴ��У�
    SCHEDULER_JOBSTORES = {'redis': RedisJobStore(host='180.76.160.45', password='admini')}
    # ����ʱ����ʱ����һ�»ᵼ�¶�ʱ�����ʱ�����
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # һ��Ҫ����API���ܣ������ſ�����api�ķ�ʽȥ�鿴���޸Ķ�ʱ����
    SCHEDULER_API_ENABLED = True
    # apiǰ׺��Ĭ����/scheduler��
    SCHEDULER_API_PREFIX = '/scheduler'
    # ��������ִ�ж�ʱ�����������
    SCHEDULER_ALLOWED_HOSTS = ['*']
    # auth��֤��Ĭ���ǹرյģ�
    SCHEDULER_AUTH = HTTPBasicAuth()
    # ���ö�ʱ�����ִ������Ĭ�������ִ������Ϊ10���̳߳أ�
    SCHEDULER_EXECUTORS = {'default': {'type': 'threadpool', 'max_workers': 10}}
    # ����flask-apscheduler������־��¼����nameΪapscheduler.scheduler��apscheduler.executors.default�������Ҫ������־������Ҫ�Դ���־��¼����������