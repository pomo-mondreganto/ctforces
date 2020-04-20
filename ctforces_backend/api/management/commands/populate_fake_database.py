import random

from django.core.management.base import BaseCommand
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
                is_published=random.choice([True, False]),
                show_on_main_page=random.choice([False] * 5 + [True])
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
            tags = list(set(random.choices(tags, k=random.randint(1, 5))))
            task = models.Task(
                author=author,
                name=fake.sentence(nb_words=2),
                description=fake.text(),
                flag=fake.sentence(nb_words=2),
                cost=random.randint(1, 1000),
                is_published=random.choice([True, False]),
                show_on_main_page=random.choice([False] * 5 + [True]),
            )
            task.save()

            task.tags.add(*tags)
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
            t = models.Team(
                captain=captain,
                name=fake.sentence(nb_words=5),
            )

            t.save()
            parts = list(set(random.choices(users, k=random.randint(0, 40))))
            if parts:
                t.participants.add(*parts)

            results.append(t)

        return results

    def handle(self, *args, **options):
        users = self.create_users(100)
        tags = self.create_tags(50)
        _ = self.create_posts(users, 100)
        tasks = self.create_tasks(users, tags, 200)
        _ = self.create_hints(users, tasks, 400)
        teams = self.create_teams(users, 300)
