from celery_tasks.main import app

@app.task(name='send_sms')
def send_sms_code(code):
    # 定义方法，封装耗时代码
    print(code)
