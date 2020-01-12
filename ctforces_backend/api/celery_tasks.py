from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.core.mail import send_mail
from django.db.models import IntegerField, Value as V, OuterRef, Q, Count, F
from django.db.models.functions import Coalesce, Ceil, Greatest
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
def start_contest(task, contest_id):
    task_id = task.request.id

    query_filter = Q(celery_start_task_id=task_id)
    if contest_id:
        query_filter &= Q(id=contest_id)

    logger.info(f'Request to start contest_id {contest_id}, task {task_id}')

    contest = get_model('api', 'Contest').objects.filter(query_filter).first()

    if not contest:
        logger.info('Contest not staring, no such contest')
        return

    logger.info(f'Starting contest {contest.id}')

    contest.is_running = True
    contest.save()


@shared_task(bind=True)
def end_contest(task, contest_id):
    task_id = task.request.id

    query_filter = Q(celery_end_task_id=task_id)
    if contest_id:
        query_filter &= Q(id=contest_id)

    logger.info(f'Request to end contest_id {contest_id}, task {task_id}')

    contest = get_model('api', 'Contest').objects.filter(query_filter).first()

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

    relation_filter = Q(contest=contest, participant__show_in_ratings=True)
    if not contest.always_recalculate_rating:
        relation_filter &= Q(has_opened_contest=True)

    participants = []
    if contest.dynamic_scoring:
        user_cost_sum_subquery = api_database_functions.SubquerySum(
            get_model('api', 'ContestTaskRelationship').objects.filter(
                contest=contest,
            ).annotate(
                solved_count=Coalesce(
                    Count(
                        'solved_by',
                        distinct=True,
                    ),
                    V(0),
                ),
            ).filter(
                solved_by__id__exact=OuterRef('participant_id'),
            ).annotate(
                current_cost=Greatest(
                    Ceil(
                        (F('min_cost') - F('max_cost')) /
                        (F('decay_value') * F('decay_value')) *
                        (F('solved_count') * F('solved_count')) +
                        F('max_cost')
                    ),
                    F('min_cost'),
                ),
            ).values('current_cost'),
            output_field=IntegerField(),
            field_name='current_cost',
        )

    else:
        user_cost_sum_subquery = api_database_functions.SubquerySum(
            get_model('api', 'ContestParticipantRelationship').objects.filter(
                contest=contest,
                solved_by__id__exact=OuterRef('id'),
            ).values('cost'),
            output_field=IntegerField(),
            field_name='cost',
        )

    relations = get_model('api', 'ContestParticipantRelationship').objects.filter(
        relation_filter,
    ).select_related(
        'participant',
    ).annotate(
        cost_sum=Coalesce(user_cost_sum_subquery, V(0)),
    ).only(
        'participant',
        'last_solve',
    ).order_by('-cost_sum', 'last_solve')

    for relation in relations:
        participant = relation.participant
        participant.cost_sum = relation.cost_sum
        participant.last_contest_solve = relation.last_solve
        participants.append(participant)

    logger.info("Got user list for rating recalculation: ", participants)

    ratings = [player.rating for player in participants]
    rs = RatingSystem(ratings)
    deltas = rs.calculate()

    for i, player in enumerate(participants):
        get_model('api', 'User').objects.filter(id=player.id).update(
            rating=player.rating + deltas[i],
            has_participated_in_rated_contest=True,
        )
        get_model('api', 'ContestParticipantRelationship').objects.filter(
            participant_id=player.id,
            contest=contest,
        ).update(
            delta=deltas[i],
        )

        if player.rating + deltas[i] > player.max_rating or not player.has_participated_in_rated_contest:
            get_model('api', 'User').objects.filter(id=player.id).update(
                max_rating=player.rating + deltas[i],
            )


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


@shared_task
def send_users_mail(subject, message, html_message, from_email, recipient_list):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
    )
