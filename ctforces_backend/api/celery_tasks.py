from celery import shared_task
from django.apps import apps
from django.db.models import Sum, Case, When, IntegerField, Value as V
from django.utils import timezone
from stdimage.utils import render_variations

from api.rating_system import RatingSystem

get_model = apps.get_model


@shared_task
def process_stdimage(file_name, variations, storage):
    render_variations(file_name, variations, replace=True, storage=storage)
    obj = get_model('api', 'User').objects.get(avatar=file_name)
    obj.save()


@shared_task
def start_contest(contest_id):
    print('Starting contest {}'.format(contest_id))
    contest = get_model('website', 'Contest').objects.filter(id=contest_id).first()

    if not contest:
        print('Contest not staring, no such contest')
        return

    contest.is_running = True
    contest.save()


@shared_task
def end_contest(contest_id):
    print('Ending contest {}'.format(contest_id))
    contest = get_model('website', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        print('Contest not ending, no such contest')
        return

    contest.is_running = False
    contest.is_finished = True
    contest.is_registration_open = False
    contest.save()

    recalculate_rating.delay(contest_id)
    publish_tasks.delay(contest_id)


@shared_task
def recalculate_rating(contest_id):
    print('Recalculation of rating for contest', contest_id)
    contest = get_model('website', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        print('No such contest')
        return

    participants = contest.participants.annotate(
        cost_sum=Sum(
            Case(
                When(
                    contest_task_relationship__contest=contest,
                    then='contest_task_relationship__cost'
                ),
                default=V(0),
                output_field=IntegerField()
            )
        )
    ).order_by(
        '-cost_sum'
    ).values_list(
        'id',
        'cost_sum',
        'rating',
        'max_rating'
    )

    ratings = [player[1] for player in participants]
    rs = RatingSystem(ratings)
    deltas = rs.calculate()

    for i, player in enumerate(participants):
        get_model('website', 'User').objects.filter(id=player[0]).update(rating=player[2] + deltas[i])
        if player[2] + deltas[i] > player[3]:
            get_model('website', 'User').objects.filter(id=player[0]).update(max_rating=player[2] + deltas[i])


@shared_task
def publish_tasks(contest_id):
    print('Publishing tasks for contest', contest_id)
    contest = get_model('website', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        print('No such contest')
        return

    contest.tasks.update(is_published=True, publication_time=timezone.now())
