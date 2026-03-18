import logging
from .models import Task

logger = logging.getLogger(__name__)


def create_task(user, title, description=""):

    logger.info("create_task_attempt", extra={
        "user": user.username,
        "id": user.id
    })

    if Task.objects.filter(user=user, title=title).exists():
        return None, "duplicate"
    
    task = Task.objects.create(
        user=user,
        title=title,
        description=description
    )
    
    logger.info("task_created", extra={
        "user": user.username,
        "id": user.id
    })

    return task, None


def get_tasks(user):

    logger.info("listing_user_tasks", extra={
        "user": user.username,
        "id": user.id
    })

    return Task.objects.filter(user=user)


def get_task(user, task_id):

    logger.info("finding_user_task", extra={
        "user": user.username,
        "id": user.id
    })

    try:
        return Task.objects.get(id=task_id, user=user)
    except Task.DoesNotExist:

        logger.warning("user_task_unexists", extra={
            "user": user.username,
            "id": user.id
        })
        return None
    
    
def update_task(task, data):

    logger.info("update_task_attempt")

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

    logger.info("task_updated_success")

    return updated


def delete_task(task):

    logger.info("delete_task_success")

    task.delete()
