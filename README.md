# 定时任务管理平台

## 简介

本项目基于flask_apsheduler实现定时任务管理，当前版本没有前端界面，通过请求api接口进行任务调度

## 文件目录

```
定时任务
    ├── app.py	#启动器
    ├── config.py	#配置
    ├── logs
    	└── runserver.log	#日志
    ├── __pycache__
    	├── config.cpython-38.pyc
    	└── task.cpython-38.pyc
    ├── task.py	#任务
    ├── workspace
    	└── test.py	#执行脚本
    └── Readme.md

```

## 文件说明

### app.py

此文件为flask的启动器

```
#此配置用来保证中文字符的转接码
app.config['JSON_AS_ASCII'] = False

。。。。。。。

#此处可以根据实际情况，编写前端界面，也可以自定义一些api
@app.route('/')
def test():
    scheduler.add_job(myfunc, 'interval', seconds=2)
    return "sucess"


def myfunc():
    print("this is a new crontab!")
    
#use_reloader=False此参数用来防止定时任务重复启动
app.run(host='127.0.0.1', port='7788', debug=True, use_reloader=False)
```



### config.py

```python3
#此配置项用来确定定时任务的存储方式
SCHEDULER_JOBSTORES
注意导包

redis：
	SCHEDULER_JOBSTORES = {'redis': RedisJobStore(host='180.76.160.45', password='admini')}
	
mysql：
	SCHEDULER_JOBSTORES  = {'default':SQLAlchemyJobStore(url='mysql+pymysql://xxx/xx')}
	
sqlite：
	SCHEDULER_JOBSTORES = {'default': SQLAlchemyJobStore(url='sqlite:///sqlite.db')}
```

apscheduler会把job序列化存到jobstores中，如果程序终止，重新启动后会读取jobstores中的job，并根据设置进行执行



如果开启身份验证的话，直接请求是会被拒绝的

![image-20210901153812701](https://gitee.com/zarathustraNIE/typora/raw/master/20210901153812.png)

通过浏览器请求会提示填写登录信息

![image-20210901153908636](https://gitee.com/zarathustraNIE/typora/raw/master/20210901153908.png)

此处可以在请求头处通过添加验证信息进行安全认证

![image-20210901154559280](https://gitee.com/zarathustraNIE/typora/raw/master/20210901154559.png)

![image-20210901154314745](https://gitee.com/zarathustraNIE/typora/raw/master/20210901154314.png)

### task.py

任务调度函数

当前的功能是执行python脚本

具体内容可以根据实际情况进行更改



## api

```python
 def _load_api(self):
        """
        Add the routes for the scheduler API.
        """
        # 获取定时任务信息
        self._add_url_route('get_scheduler_info', '', api.get_scheduler_info, 'GET')
        # 添加任务
        self._add_url_route('add_job', '/jobs', api.add_job, 'POST')
        # 获取任务
        self._add_url_route('get_job', '/jobs/<job_id>', api.get_job, 'GET')
        self._add_url_route('get_jobs', '/jobs', api.get_jobs, 'GET')
        self._add_url_route('delete_job', '/jobs/<job_id>', api.delete_job, 'DELETE')
        self._add_url_route('update_job', '/jobs/<job_id>', api.update_job, 'PATCH')
        self._add_url_route('pause_job', '/jobs/<job_id>/pause', api.pause_job, 'POST')
        self._add_url_route('resume_job', '/jobs/<job_id>/resume', api.resume_job, 'POST')
        # 立即执行一次定时任务
        self._add_url_route('run_job', '/jobs/<job_id>/run', api.run_job, 'POST')
```

### GET_JOBS

请求当前的jobs

![image-20210901145434272](https://gitee.com/zarathustraNIE/typora/raw/master/20210901145443.png)

### ADD_JOB

请求添加jobs

此处是添加的所要执行脚本的路径，在使用时可以根据实际情况进行设置

![image-20210901150154103](https://gitee.com/zarathustraNIE/typora/raw/master/20210901150154.png)

可以看到后台正在执行对应的任务

![image-20210901150257073](https://gitee.com/zarathustraNIE/typora/raw/master/20210901150257.png)

### PAUSE_JOB

发送暂停请求

![image-20210901150411342](https://gitee.com/zarathustraNIE/typora/raw/master/20210901150411.png)

## JOB

### job参数

对job的相关参数进行介绍

```
 add_job(func, trigger=None, args=None, kwargs=None, id=None, \
            name=None, misfire_grace_time=undefined, coalesce=undefined, \
            max_instances=undefined, next_run_time=undefined, \
            jobstore='default', executor='default', \
            replace_existing=False, **trigger_args)

        Adds the given job to the job list and wakes up the scheduler if it's already running.

        Any option that defaults to ``undefined`` will be replaced with the corresponding default
        value when the job is scheduled (which happens when the scheduler is started, or
        immediately if the scheduler is already running).

        The ``func`` argument can be given either as a callable object or a textual reference in
        the ``package.module:some.object`` format, where the first half (separated by ``:``) is an
        importable module and the second half is a reference to the callable object, relative to
        the module.

        The ``trigger`` argument can either be:
          #. the alias name of the trigger (e.g. ``date``, ``interval`` or ``cron``), in which case
            any extra keyword arguments to this method are passed on to the trigger's constructor
          #. an instance of a trigger class

        :param func: callable (or a textual reference to one) to run at the given time
        :param str|apscheduler.triggers.base.BaseTrigger trigger: trigger that determines when
            ``func`` is called
        :param list|tuple args: list of positional arguments to call func with
        :param dict kwargs: dict of keyword arguments to call func with
        :param str|unicode id: explicit identifier for the job (for modifying it later)
        :param str|unicode name: textual description of the job
        :param int misfire_grace_time: seconds after the designated runtime that the job is still
            allowed to be run (or ``None`` to allow the job to run no matter how late it is)
        :param bool coalesce: run once instead of many times if the scheduler determines that the
            job should be run more than once in succession
        :param int max_instances: maximum number of concurrently running instances allowed for this
            job
        :param datetime next_run_time: when to first run the job, regardless of the trigger (pass
            ``None`` to add the job as paused)
        :param str|unicode jobstore: alias of the job store to store the job in
        :param str|unicode executor: alias of the executor to run the job with
        :param bool replace_existing: ``True`` to replace an existing job with the same ``id``
            (but retain the number of runs from the existing one)
        :rtype: Job
```

```
func：				callable (or a textual reference to one) to run at the given time
trigger：			str|apscheduler.triggers.base.BaseTrigger trigger: trigger that determines when
            				``func`` is called					#触发器，``date``, ``interval`` or ``cron``
args：				list|tuple args: list of positional arguments to call func with
kwargs：				dict kwargs: dict of keyword arguments to call func with
id：					str|unicode id: explicit identifier for the job (for modifying it later)
name：				str|unicode name: textual description of the job
misfire_grace_time：	int misfire_grace_time: seconds after the designated runtime that the job is still
            			allowed to be run (or ``None`` to allow the job to run no matter how late it is)
coalesce			bool coalesce: run once instead of many times if the scheduler determines that the
            			job should be run more than once in succession
max_instances		int max_instances: maximum number of concurrently running instances allowed for this
           							 job
next_run_time		datetime next_run_time: when to first run the job, regardless of the trigger (pass
          				  ``None`` to add the job as paused)
jobstore			str|unicode jobstore: alias of the job store to store the job in
executor			str|unicode executor: alias of the executor to run the job with
replace_existing	bool replace_existing: ``True`` to replace an existing job with the same ``id``
            			(but retain the number of runs from the existing one)
**trigger_args		Job
```



### job示例

```
 JOBS = [
        # interval定时执行（从start_date到end_date，间隔20s，包含首尾）
        # func也可以写字符串形式，例如：'App.tasks.DatabaseTask:send_ding_test'
        {
            'id': 'job2',
            'func': send_ding_test,
            'trigger': 'interval',
            'start_date': '2021-01-27 13:31:00',
            'end_date': '2021-01-27 13:33:00',
            'seconds': 20,
            'replace_existing': True  # 重新执行程序时，会将jobStore中的任务替换掉
        },
        # date一次执行
        {
            'id': 'job1',
            'func': send_ding_test,
            'trigger': 'date',
            'run_date': '2021-01-30 11:22:00',
            'replace_existing': True
        },
        # cron式定时调度，类似linux的crontab
        {
            'id': 'job3',
            'func': send_ding_test,
            'trigger': 'cron',
            'day_of_week': '0-6',
            'month': '*',
            'hour': '6',
            'minute': '0',
            'second': '0',
            'replace_existing': True
        }

    ]

```

### 触发器

下面的三种触发器的参数详解

#### interval

`interval` 对应 `apscheduler.triggers.interval.IntervalTrigger` 类, 下面是它的初始化方法:redis

```
IntervalTrigger(weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, end_date=None, timezone=None, jitter=None)

其中的 初始化参数 是须要在 task 装饰器中传入的 关键字参数. 其中 run_date 表示任务开始执行时间, 若是为 None 则从任务生成时开始算起, end_date 是结束时间, 到达这个时间点后, 任务将中止. 如下是每个参数的含义:

weeks(int): 须要等待的周数
days(int): 须要等待的天数
hours(int): 须要等待的小时数
minutes(int): 须要等待的分钟数
seconds(int): 须要等待的秒数
start_data(datetime|str): 任务开始时间
end_date(datetime|str): 任务结束时间
timezone(datetime.tzinfo|str): 时区
jitter(int|None): 延迟窗口, 设置此值后, 真正的间隔时间将在 ±jitter 间浮动
```

#### cron

`cron` 对应 `apscheduler.triggers.cron.CronTrigger` 类, 下面是它的初始化方法:

```
CronTrigger(year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None, second=None, start_date=None, end_date=None, timezone=None, jitter=None)

最后四个参数与 interval 一致, 再也不解释, 如下为每一个参数的含义:
year(int|str): YYYY 格式的年
month(int|str): 1-12 月
day(int|str): 1-31 天
week(int|str): 1-53 周
day_of_week(int|str): 一周的某一天, 能够为 数字 或者 名字
数字为 0-6,
名字为 mon,tue,wed,thu,fri,sat,sun
hour(int|str): 0-23 小时
minute(int|str): 0-59 分钟
second(int|str): 0-59 秒
```

cron 是 Apscheduler 中最强大的 trigger, 它的使用方式相似于 linux 下的 crontab, 因此以上参数的值可使用 cron 表达式 设置, 如下为可用的表达式, 表格中 任意字段 的 含义 将以 秒 进行解释, 使用时表示具体使用的 参数字段

| 表达式   | 参数字段 | 含义                                                   |
| :------- | :------- | :----------------------------------------------------- |
| `*`      | 任意     | 任意秒, 即每秒执行                                     |
| `*/a`    | 任意     | 当前秒数为 `a` 的倍数时执行                            |
| `a-b`    | 任意     | 当前秒数在 `a` 和 `b` 之间时执行                       |
| `a-b/c`  | 任意     | 当前秒数在 `a` 和 `b` 之间且是 `c` 的倍数时执行        |
| `xth y`  | day      | 这个月第 `x` 个 `周`, 例如 `3rd mon` 表示 `第三个周一` |
| `last x` | day      | 这个月最后一个 `周`                                    |
| `last`   | day      | 这个月最后的一天                                       |
| `x,y,z`  | 任意     | 以上表达式能够写多个, 逗号分隔                         |

在设置参数时，没有设置的参数将设置默认值. 默认参数规则以一个例子解释. 若是定义 `day=1, minute=20` 两个字段, 则这两个字段中 `含义` 最小的为 `minute`, 而后比 `minute` 小的字段设为 `最小值`, 比它大的字段设置为 `*`, 可是 `week` 和 `day_of_week` 一直设置为 `*`. 因此比 `minute` 小的字段 `second` 设置为 `0`, 其余设置为 `*`. 以上例子对应的结果为:

```
year='*', month='*', day=1, week='*', day_of_week='*', hour='*', minute=20, second=0
```

#### date

`date` 比较简单, 只有一个 `run_date` 参数, 用于设置执行时间, 只执行一次.