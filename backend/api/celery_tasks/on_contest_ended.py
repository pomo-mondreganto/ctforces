from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.db.transaction import atomic

from .publish_tasks import publish_tasks
from .recalculate_rating import recalculate_rating

get_model = apps.get_model

logger = get_task_logger(__name__)


@shared_task
def on_contest_ended(contest_id):
    with atomic():
        contest = get_model('api', 'Contest').objects.filter(id=contest_id).select_for_update().first()

        if not contest:
            logger.error('No such contest')
            return

        if contest.processed_end_task:
            logger.warning('End task already run')

        contest.processed_end_task = True
        contest.is_registration_open = False
        contest.save(update_fields=['processed_end_task', 'is_registration_open', 'updated_at'])

    if contest.is_rated:
        recalculate_rating.delay(contest.id)

    if contest.publish_tasks_after_finished:
        publish_tasks.delay(contest.id)
