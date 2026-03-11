from .models import Task


def create_task(user, title, description=""):

    if Task.objects.filter(user=user, title=title).exists():
        return None, "duplicate"
    
    task = Task.objects.create(
        user=user,
        title=title,
        description=description
    )

    return task, None


def get_tasks(user):

    return Task.objects.filter(user=user)


def get_task(user, task_id):

    try:
        return Task.objects.get(id=task_id, user=user)
    except Task.DoesNotExist:
        return None
    
    
def update_task(task, data):

    updated = False

    if "title" in data and data["title"].strip():
        task.title = data["title"]
        updated = True

    if "description" in data:
        task.description = data["description"] or ""
        updated = True

    if "is_done" in data and isinstance(data["is_done"], bool):
        task.is_done = data["is_done"]
        updated = True

    if updated:
        task.save()

    return updated


def delete_task(task):

    task.delete()