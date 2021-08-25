from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.db.models.functions import Greatest
from django.utils import timezone
from stdimage.utils import render_variations

from api.rating_system import RatingSystem

get_model = apps.get_model

logger = get_task_logger(__name__)


@shared_task
def process_stdimage(file_name, variations, storage):
    render_variations(file_name, variations, replace=True, storage=storage)
    obj = get_model('api', 'User').objects.get(avatar=file_name)
    obj.save()


@shared_task
def start_contest(contest_id):
    logger.info(f'Request to start contest_id {contest_id}')

    contest = get_model('api', 'Contest').objects.filter(id=contest_id).first()

    if not contest:
        logger.info(f'Contest {contest_id} not starting, no such contest')
        return

    if contest.is_running:
        logger.info(f'Contest {contest_id} not starting, already started')
        return

    logger.info(f'Starting contest {contest.id}')

    contest.is_running = True
    contest.save(update_fields=['is_running', 'updated_at'])


@shared_task
def end_contest(contest_id):
    logger.info(f'Request to end contest_id {contest_id}')

    contest = get_model('api', 'Contest').objects.filter(id=contest_id).first()

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
    contest.save(update_fields=['is_running', 'is_finished', 'is_registration_open', 'updated_at'])

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

    relations = contest.get_scoreboard_relations_queryset().prefetch_related(
        'registered_users',
    )

    teams = []
    for relation in relations:
        team = relation.participant
        team.cost_sum = relation.cost_sum
        team.last_contest_solve = relation.last_solve

        team.players = sorted(
            list(
                relation.registered_users.all()
            ),
            key=lambda x: x.rating,
            reverse=True,
        )
        teams.append(team)

    logger.info(f"Got team list for rating recalculation: {teams}")

    players = []
    team_ratings = []
    player_ratings = []
    for i, team in enumerate(teams):
        team_ratings.append((i + 1, team.rating))
        players.extend(team.players)
        player_ratings.extend(((i + 1, player.rating) for player in team.players))

    logger.info(f"Team rating data: {team_ratings}")
    logger.info(f"Player rating data: {player_ratings}")

    team_rs = RatingSystem(team_ratings)
    player_rs = RatingSystem(player_ratings)
    team_deltas = team_rs.calculate()
    player_deltas = player_rs.calculate()

    for team, delta in zip(teams, team_deltas):
        get_model('api', 'Team').objects.filter(id=team.id).update(
            rating=F('rating') + delta,
            max_rating=Greatest(F('max_rating'), F('rating') + delta),
        )
        get_model('api', 'ContestParticipantRelationship').objects.filter(
            participant=team,
            contest=contest,
        ).update(delta=delta)

    for player, delta in zip(players, player_deltas):
        get_model('api', 'User').objects.filter(id=player.id).update(
            rating=F('rating') + delta,
            max_rating=Greatest(F('max_rating'), F('rating') + delta),
        )

    logger.info(f'Done recalculating rating for contest {contest_id}')


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
def send_users_mail(subject, text_message, html_message, recipient_list):
    if settings.EMAIL_MODE == 'smtp':
        send_mail(
            subject=subject,
            message=text_message,
            from_email=None,
            recipient_list=recipient_list,
            html_message=html_message,
        )
    elif settings.EMAIL_MODE == 'sendgrid':
        pass
        # TODO: send emails with sendgrid
    else:
        raise ValueError('Sending emails is disabled in current environment')
