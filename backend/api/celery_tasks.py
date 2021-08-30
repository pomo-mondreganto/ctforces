from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.db.models.functions import Greatest
from django.db.transaction import atomic
from django.utils import timezone
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
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
def on_contest_ended(contest_id):
    with atomic:
        contest = get_model('api', 'Contest').objects.filter(id=contest_id).select_for_update().first()

        if not contest:
            logger.error('No such contest')
            return

        if contest.processed_end_task:
            logger.warning('End task already run')

        contest.processed_end_task = True
        contest.is_registration_open = False
        contest.save(update_fields=['end_task', 'is_registration_open', 'updated_at'])

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

    if not contest.always_recalculate_rating:
        relations = relations.filter(opened_contest_at__isnull=False)

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
        logger.info('Sending email to %s with smtp', recipient_list)
        send_mail(
            subject=subject,
            message=text_message,
            from_email=None,
            recipient_list=recipient_list,
            html_message=html_message,
        )
    elif settings.EMAIL_MODE == 'sendgrid':
        logger.info('Sending email to %s with sendgrid', recipient_list)
        message = Mail(
            to_emails=recipient_list,
            subject=subject,
            html_content=html_message,
            plain_text_content=text_message,
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        logger.debug('Received sendgrid response: %s', response)
    else:
        raise ValueError('Sending emails is disabled in current environment')
