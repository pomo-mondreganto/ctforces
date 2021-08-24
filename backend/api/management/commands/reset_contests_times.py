from django.core.management.base import BaseCommand

from api.celery_tasks import start_contest, end_contest
from api.models import Contest
from ctforces.celery import app as celery_app


class Command(BaseCommand):
    help = 'Resets all old start & end tasks and creates new ones for every NOT finished contest'

    def handle(self, *args, **options):
        unfinished_contests = Contest.objects.filter(is_finished=False)
        unstarted_contests = unfinished_contests.filter(is_running=False)

        for contest in unstarted_contests:
            self.stdout.write(f'Processing unstarted contest {contest}')
            celery_app.control.revoke(contest.celery_start_task_id)
            contest.celery_start_task_id = start_contest.apply_async(
                args=(contest.id,),
                eta=contest.start_time,
            )
            contest.save()

        for contest in unfinished_contests:
            self.stdout.write(f'Processing unfinished contest {contest}')
            celery_app.control.revoke(contest.celery_end_task_id)
            contest.celery_end_task_id = end_contest.apply_async(
                args=(contest.id,),
                eta=contest.end_time,
            )
            contest.save()

        self.stdout.write('Done!')
