from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.core.mail import send_mail
from django.db.models import IntegerField, Value as V, Q, Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.utils import timezone
from stdimage.utils import render_variations

from api import database_functions as api_database_functions
from api.rating_system import RatingSystem

get_model = apps.get_model

logger = get_task_logger(__name__)


@shared_task
def process_stdimage(file_name, variations, storage):
    render_variations(file_name, variations, replace=True, storage=storage)
    obj = get_model('api', 'User').objects.get(avatar=file_name)
    obj.save()


@shared_task(bind=True)
def start_contest(self, contest_id):
    logger.info(f'Request to contest_id {contest_id}, task {self.request.id}')

    query = Q(celery_start_task_id=self.request.id)
    if contest_id:
        query &= Q(id=contest_id)

    contest = get_model('api', 'Contest').objects.filter(query).first()

    if not contest:
        logger.info('Contest not staring, no such contest')
        return

    logger.info(f'Starting contest {contest.id}')

    contest.is_running = True
    contest.save()


@shared_task(bind=True)
def end_contest(self, contest_id):
    logger.info('Request to end contest_id {}, task {}'.format(contest_id, self.request.id))

    query = Q(celery_end_task_id=self.request.id)
    if contest_id:
        query &= Q(id=contest_id)

    contest = get_model('api', 'Contest').objects.filter(query).first()

    if not contest:
        logger.info('Contest not ending, no such contest')
        return

    logger.info(f'Ending contest {contest.id}')

    if contest.is_finished:
        logger.info('Contest has already ended')
        return

    contest.is_running = False
    contest.is_finished = True
    contest.is_registration_open = False
    contest.save()

    if contest.is_rated:
        recalculate_rating.delay(contest.id)

    if contest.publish_tasks_after_finished:
        publish_tasks.delay(contest.id)


@shared_task
def recalculate_rating(contest_id):
    logger.info(f'Recalculation of rating for contest {contest_id}')
    contest = get_model('api', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        logger.info('No such contest')
        return

    contest_cost_subquery = Subquery(
        get_model('api', 'ContestTaskRelationship').objects.filter(
            contest_id=contest.id,
            task_id=OuterRef('task_id'),
        ).values('cost'),
        output_field=IntegerField(),
    )

    user_cost_sum_subquery = api_database_functions.SubquerySum(
        get_model('api', 'ContestTaskParticipantSolvedRelationship').objects.filter(
            contest_id=contest.id,
            participant_id=OuterRef('id'),
        ).annotate(
            cost=Coalesce(
                contest_cost_subquery,
                V(0),
            )
        ).values('cost'),
        output_field=IntegerField(),
        field_name='cost',
    )

    last_contest_solve_subquery = Subquery(
        get_model('api', 'ContestParticipantRelationship').objects.filter(
            contest=contest,
            participant=OuterRef('id'),
        ).values('last_solve')
    )

    participants = contest.participants.annotate(
        cost_sum=Coalesce(
            user_cost_sum_subquery,
            V(0),
        ),
        last_contest_solve=last_contest_solve_subquery,
    ).order_by(
        '-cost_sum',
        'last_contest_solve',
    ).values_list(
        'id',
        'cost_sum',
        'rating',
        'max_rating',
    )

    ratings = [player[2] for player in participants]
    rs = RatingSystem(ratings)
    deltas = rs.calculate()

    for i, player in enumerate(participants):
        get_model('api', 'User').objects.filter(id=player[0]).update(rating=player[2] + deltas[i])
        get_model('api', 'ContestParticipantRelationship').objects.filter(
            user_id=player[0],
            contest_id=contest_id
        ).update(
            delta=deltas[i]
        )

        if player[2] + deltas[i] > player[3] or player.contest_participant_relationship.count() == 1:
            get_model('api', 'User').objects.filter(id=player[0]).update(max_rating=player[2] + deltas[i])


@shared_task
def publish_tasks(contest_id):
    logger.info(f'Publishing tasks for contest {contest_id}')
    contest = get_model('api', 'Contest').objects.filter(id=contest_id).first()
    if not contest:
        logger.info('No such contest')
        return

    contest.tasks.update(is_published=True, publication_time=timezone.now())


@shared_task
def send_users_mail(subject, message, html_message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
    )
