import random

from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone, now
from faker import Faker

from api import models as models

fake = Faker()


class Command(BaseCommand):
    help = 'Creates fake demonstration models'

    @staticmethod
    def create_users(count):
        results = []

        for _ in range(count):
            username = fake.simple_profile()['username']
            username += fake.pystr(max_chars=15 - len(username))
            u = models.User(
                email=fake.email(),
                username=username,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password=fake.password(),
            )
            u.save()
            results.append(u)

        return results

    @staticmethod
    def create_posts(users, count):
        results = []

        for _ in range(count):
            author = random.choice(users)
            p = models.Post(
                author=author,
                title=fake.sentence(),
                body=fake.text(),
                is_published=fake.pybool(),
                show_on_main_page=fake.pybool(),
            )
            p.save()
            results.append(p)
        return results

    @staticmethod
    def create_tags(count):
        results = []

        for _ in range(count):
            t = models.TaskTag(
                name=fake.lexify('?' * random.randint(3, 10)),
            )
            t.save()

            results.append(t)
        return results

    @staticmethod
    def create_tasks(users, tags, count):
        results = []

        for _ in range(count):
            author = random.choice(users[:20])
            solved = list(set(random.choices(users[20:], k=random.randint(1, 50))))
            task_tags = list(set(random.choices(tags, k=random.randint(1, 5))))
            task = models.Task(
                author=author,
                name=fake.sentence(nb_words=2),
                description=fake.text(),
                flag=fake.sentence(nb_words=2),
                cost=random.randint(1, 1000),
                is_published=random.choice([True, False]),
                show_on_main_page=random.choice([False] * 3 + [True]),
            )
            task.save()

            task.tags.add(*task_tags)
            task.solved_by.add(*solved)

            results.append(task)
        return results

    @staticmethod
    def create_hints(users, tasks, count):
        results = []

        for _ in range(count):
            author = random.choice(users)
            task = random.choice(tasks)
            h = models.TaskHint(
                author=author,
                task=task,
                body=fake.text(),
                is_published=random.choice([True, False]),
            )

            h.save()
            results.append(h)

        return results

    @staticmethod
    def create_teams(users, count):
        results = []

        for _ in range(count):
            captain = random.choice(users)
            name = fake.sentence(nb_words=4)[:25]
            rating = random.randint(0, 5000)
            t = models.Team(
                captain=captain,
                name=name,
                join_token=models.Team.gen_join_token(name),
                rating=rating,
                max_rating=rating,
            )

            t.save()
            parts = list(set(random.choices(users, k=random.randint(0, 40)) + [captain]))
            if parts:
                t.participants.add(*parts)

            results.append(t)

        return results

    @staticmethod
    def create_contests(users, teams, tasks, count):
        results = []

        for _ in range(count):
            author = random.choice(users)
            end_time = fake.date_time_this_year(before_now=True, after_now=True, tzinfo=get_current_timezone())
            start_time = fake.date_time_between(start_date='-1y', end_date=end_time, tzinfo=get_current_timezone())
            running = (end_time > now() >= start_time)
            finished = end_time <= now()
            c = models.Contest(
                author=author,
                name=fake.sentence(nb_words=2),
                description=fake.text(),
                start_time=start_time,
                end_time=end_time,
                is_published=fake.pybool(),
                is_running=running,
                is_finished=finished,
                is_registration_open=fake.pybool(),
                publish_tasks_after_finished=fake.pybool(),
                is_rated=fake.pybool(),
                always_recalculate_rating=fake.pybool(),
                dynamic_scoring=fake.pybool(),
            )

            c.save()

            participants = list(set(random.choices(teams, k=random.randint(1, 50))))
            for team in participants:
                team_members = team.participants.all()
                registered_users = list(set(random.choices(team_members, k=random.randint(1, len(team_members)))))

                rel = models.ContestParticipantRelationship(contest=c, participant=team)
                rel.save()

                rel.registered_users.add(*registered_users)

                to_create = []
                for u in registered_users:
                    helper = models.CPRHelper(
                        contest=c,
                        user=u,
                        cpr=rel,
                    )
                    to_create.append(helper)
                models.CPRHelper.objects.bulk_create(to_create, ignore_conflicts=True)

            chosen_tasks = list(set(random.choices(tasks, k=random.randint(1, 50))))
            for task in chosen_tasks:
                rel = models.ContestTaskRelationship(
                    contest=c,
                    task=task,
                    main_tag=random.choice(task.tags.all()),
                    cost=fake.pyint(1, 1000),
                    min_cost=fake.pyint(1, 500),
                    max_cost=fake.pyint(501, 1000),
                    decay_value=fake.pyint(1, 100),
                )
                rel.save()

                if running or finished:
                    solved = list(set(random.choices(participants, k=random.randint(1, len(participants)))))
                    rel.solved_by.add(*solved)

            results.append(c)

        return results

    def handle(self, *args, **options):
        users = self.create_users(200)
        tags = self.create_tags(20)
        _ = self.create_posts(users, 200)
        tasks = self.create_tasks(users, tags, 200)
        _ = self.create_hints(users, tasks, 400)
        teams = self.create_teams(users, 300)
        _ = self.create_contests(users=users, teams=teams, tasks=tasks, count=100)
