import os
import shutil

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from api.models import Task


class Command(BaseCommand):
    dump_dir = '/tmp/tasks_dump'
    help = (
        f'Dumps all tasks to {dump_dir}'
    )

    def handle(self, *args, **options):
        shutil.rmtree(self.dump_dir, ignore_errors=True)
        os.mkdir(self.dump_dir)
        qs = Task.objects.all().select_related(
            'author',
        ).prefetch_related(
            'tags',
            'files',
            'solved_by',
        ).order_by(
            'id',
        )
        for task in qs:
            dirname = f'{task.id:03}_{slugify(task.name)}'
            task_dir = os.path.join(self.dump_dir, dirname)
            os.mkdir(task_dir)

            tags = ", ".join(tag.name for tag in task.tags.all())
            solved_by = ', '.join(user.username for user in task.solved_by.all())
            padding = '@' * 40
            data_contents = (
                f'Name: {task.name}\n'
                f'Cost: {task.cost}\n'
                f'Flag: {task.flag}\n'
                f'Tags: {tags}\n'
                f'Description:\n{padding}\n{task.description}\n{padding}\n'
                f'Solved by: {solved_by}\n'
                f'Author: {task.author.username}\n'
            )

            data_path = os.path.join(task_dir, 'data.txt')
            with open(data_path, 'w') as f:
                f.write(data_contents)

            files = list(task.files.all())
            if files:
                files_dir = os.path.join(task_dir, 'files')
                os.mkdir(files_dir)

                file_names = [file.name for file in files]
                assert len(set(file_names)) == len(file_names)

                for file in files:
                    res_path = os.path.join(files_dir, file.name)
                    shutil.copy2(file.file_field.url, res_path)

            if task.id % 10 == 0:
                self.stdout.write(f'Done {task.id}')
