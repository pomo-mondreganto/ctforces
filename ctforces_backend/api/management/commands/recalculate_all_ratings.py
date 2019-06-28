from django.core.management.base import BaseCommand

from api import celery_tasks as api_tasks
from api import models as api_models


class Command(BaseCommand):
    help = (
        'Resets ratings to default values for all users, '
        'then calls rating recalculation for all finished contests '
        'ordered by id descending'
    )

    def handle(self, *args, **options):
        default_rating = api_models.User._meta.get_field('rating').get_default()

        self.stdout.write(f'Resetting rating to default {default_rating}')
        api_models.User.objects.update(rating=default_rating, max_rating=default_rating)

        self.stdout.write(f'Querying finished contests')
        contest_ids = api_models.Contest.objects.filter(
            is_finished=True,
            is_rated=True
        ).order_by('id').values_list('id', flat=True)

        self.stdout.write(f'Got {len(contest_ids)} contests')

        self.stdout.write(f'Starting reting recalculation')
        for i, contest_id in enumerate(contest_ids):
            api_tasks.recalculate_rating(contest_id)
            self.stdout.write(f'Contest {contest_id} done, {len(contest_ids) - i - 1} left')

        self.stdout.write('Done recalculation')
