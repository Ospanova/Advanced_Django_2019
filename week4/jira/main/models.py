from django.db import models

from main import constants
from users.models import MainUser


class Project(models.Model):
    name = models.CharField(max_length=21)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MemberProject(models.Model):
    member = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Block(models.Model):
    name = models.CharField(max_length=21)
    type = models.CharField(max_length=11, choices=constants.BLOCK_TYPES, default=constants.TODO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_blocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskManager(models.Manager):
    def tasks_by_block(self, block):
        return self.filter(block=block)

    def tasks_by_creator_and_block(self, block, user):
        return self.filter(block=block, creator=user)

    def tasks_by_executor_and_block(self, block, user):
        return self.filter(block=block, executor=user)


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    order = models.IntegerField(blank=True, default=None)
    block = models.ForeignKey(Block, on_delete=models.DO_NOTHING, related_name='block_tasks')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskDocument(models.Model):
    document = models.FileField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_documents')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
