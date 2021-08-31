from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.utils import timezone

get_model = apps.get_model

logger = get_task_logger(__name__)


@shared_task
def publish_tasks(contest_id):
    logger.info(f'Publishing tasks for contest {contest_id}')
    contest = get_model('api', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        logger.info('No such contest')
        return

    contest.tasks.update(
        show_on_main_page=True,
        publication_time=timezone.now(),
        is_published=True,
    )
