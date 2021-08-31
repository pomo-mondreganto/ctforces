from celery import shared_task
from celery.utils.log import get_task_logger
from django.apps import apps
from django.db.models import F
from django.db.models.functions import Greatest

from api.rating_system import RatingSystem

get_model = apps.get_model

logger = get_task_logger(__name__)


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
