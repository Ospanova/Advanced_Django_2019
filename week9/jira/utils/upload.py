def task_document_path(instance, filename):
    task_id = instance.task.id
    project_id = instance.task.block.project.id
    return f'projects/project_{project_id}/task_{task_id}/{filename}'
