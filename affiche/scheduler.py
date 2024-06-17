import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.utils import timezone
from .models import Performance

# Настройка логирования
logger = logging.getLogger(__name__)


def my_scheduled_job():
    now = timezone.now()
    performances = Performance.objects.filter(hidden=False)
    for performance in performances:
        if performance.datetime1 and performance.datetime1 < now:
            performance.datetime1 = performance.datetime2
            performance.datetime2 = None
            logger.debug(f'Updated performance {performance.id}: datetime1 set to datetime2')

        elif performance.datetime2 and performance.datetime2 < now:
            performance.datetime2 = None
            logger.debug(f'Updated performance {performance.id}: datetime2 cleared')

        if performance.datetime1 or performance.datetime2:
            performance.hidden = False
            logger.debug(f'Updated performance {performance.id}: hidden set to False')
        else:
            performance.hidden = True
            logger.debug(f'Updated performance {performance.id}: hidden set to True')

        performance.save()
        logger.debug(f'Saved performance {performance.id}')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        my_scheduled_job,
        "interval",
        minutes=24 * 60,
        id='my_scheduled_job',
        replace_existing=True
    )

    register_events(scheduler)
    scheduler.start()
    logger.info('Scheduler started')
