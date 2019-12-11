from django.db import models
from users.models import MainUser
from utils.constants import TASK_STATUSES, TASK_NEW
from utils.validators import *
from utils.upload import *
from django.db.models import Q

class ProjectManager(models.Manager):
    def filter_by_name(self, name):
        return super(ProjectManager, self).get_queryset().filter(name__contains=name)

    def my_projects(self, user):
        return super(ProjectManager, self).get_queryset().filter(creator=user)

    def order_by_name(self):
        return super(ProjectManager, self).get_queryset().order_by('name')

class Project(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_projects')
    objects = models.Manager()
    projects = ProjectManager()

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=300)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')
    status = models.PositiveSmallIntegerField(choices=TASK_STATUSES, default=TASK_NEW)
    @property
    def tasks_count(self):
        return self.blocks.count()

    def __str__(self):
        return f'{self.name}({self.project})'


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='involved_projects')

    def __str__(self):
        return self.user.username

class TaskManager(models.Manager):
    def tasks_for_me(self, user):
        return super().get_queryset().filter(Q(creator=user) | Q(executor=user))

    def my_tasks(self, user):
        return super().get_queryset().filter(creator=user)

    def tasks_to_execute(self, user):
        return super().get_queryset().filter(executor=user)


class Task(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='executed_tasks')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')
    order = models.IntegerField()
    tasks = TaskManager()

    def __str__(self):
        return f'Task {self.id} "{self.name}"({self.creator})'


class TaskDocument(models.Model):
    document = models.FileField(upload_to=task_document_path, validators=[validate_file_size, validate_extension],
                                null=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='task_documents')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f'{self.task}(document #){self.id}'


class TaskComment(models.Model):
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='task_comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.body}({self.creator})'

    def save(self, *args, **kwargs):
        created = self.pk is None
        if created:
            if self.creator.is_superuser:
                self.stars = 10
        super().save(*args, **kwargs)