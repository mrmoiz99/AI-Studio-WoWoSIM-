from apscheduler.schedulers.background import BackgroundScheduler
from trends.collector import collect_trends

scheduler = BackgroundScheduler()

def start_daily_collection(hour=8, minute=0):
    if not scheduler.running:
        scheduler.start()
    scheduler.add_job(collect_trends, 'cron', hour=hour, minute=minute, id='daily_trends', replace_existing=True)
    return True
