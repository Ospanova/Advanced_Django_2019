import shutil
import os


def task_document_path(instance, filename):
    project_id = instance.task.project.id
    task_id = instance.task.id
    return f'projects/{project_id}/{task_id}/{filename}'


def avatar_document_path(instance, filename):
    profile_id = instance.id
    return f'profile_avatars/{profile_id}/{filename}'


def delete_path(document):
    print(document)
    task_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(task_path)
