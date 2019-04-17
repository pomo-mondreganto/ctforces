from django.core.management.base import BaseCommand

from api import celery_tasks as api_tasks
from api import models as api_models
from ctforces_backend.celery import app as celery_app


class Command(BaseCommand):
    help = 'Resets all old start & end tasks and creates new ones for every NOT finished contest'

    def handle(self, *args, **options):
        unstarted_contests = api_models.Contest.objects.filter(is_running=False, is_finished=False)
        unfinished_contests = unstarted_contests.filter(is_finished=False)

        for contest in unstarted_contests:
            self.stdout.write(f'Processing unstarted contest {contest}')
            celery_app.control.revoke(contest.celery_start_task_id)
            contest.celery_start_task_id = api_tasks.start_contest.apply_async(
                args=(contest.id,),
                eta=contest.start_time,
            )
            contest.save()

        for contest in unfinished_contests:
            self.stdout.write(f'Processing unfinished contest {contest}')
            celery_app.control.revoke(contest.celery_end_task_id)
            contest.celery_end_task_id = api_tasks.end_contest.apply_async(
                args=(contest.id,),
                eta=contest.end_time,
            )
            contest.save()

        self.stdout.write('Done!')
