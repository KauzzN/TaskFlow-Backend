import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.decorators import jwt_required
from .models import Task

from .services import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)

from .utils import parse_json_body, serialize_task

logger = logging.getLogger(__name__)

@csrf_exempt
@jwt_required
def tasks_view(request):

    if request.method =="GET":

        logger.info("read_task_attempt")

        tasks = Task.objects.filter(user=request.user)
        task_list = [serialize_task(task) for task in tasks]

        logger.info("read_task_success", extra={
            "user": request.user.username,
            "id": request.user.id
        })

        return JsonResponse({
            "count": len(task_list),
            "tasks": task_list
        })
    
    elif request.method == "POST":
       
        logger.info("create_task_attempt", extra={
            "user": request.user.username,
            "id": request.user.id
        })

        data, error = parse_json_body(request)
        if error:
            return error
        
        title = data.get("title")
        description = data.get("description", "")

        if not title:
            logger.warning("create_task_title_empty")

            return JsonResponse({
                "error": "titulo obrigatorio"
            }, status=400)
        
        task, duplicate = create_task(request.user, title, description)

        if duplicate:
            
            logger.warning("task_already_exists")

            return JsonResponse({
                "error": "você ja possui uma task com esse titulo"
            }, status=409)

        logger.info("create_task_success", extra={
            "title": title,
            "user": request.user.username,
            "id": request.user.id
        })

        return JsonResponse({
            "message": "task criada com sucesso",
            "task": serialize_task(task)
        }, status=201)
    
    logger.warning("tasks_view_session_method_not_allowed", extra={
        "method": request.method
    })
    return JsonResponse({"error": "método não permitido"}, status=405)


@csrf_exempt
@jwt_required
def task_detail_view(request, task_id):

    task = get_task(request.user, task_id)

    if not task:

        logger.warning("task_unidentified")

        return JsonResponse({
            "error": "task não encontrada"
        }, status=404)

    if request.method == "GET":

        return JsonResponse({
            "task": serialize_task(task)
        })
    
    elif request.method == "PATCH":

        data, error = parse_json_body(request)
        if error:
            return error

        if not task:

            logger.warning("task_unidentified")

            return JsonResponse({
                "error": "task não encontrada"
            }, status=404)
        
        updated = update_task(task, data)

        if not updated:

            logger.info("no_tasks_updated")

            return JsonResponse({
                "message": "nenhuma alteração realizada"
            })
        
        logger.info("task_updaed_success", extra={
            "user": request.user.username,
            "id": request.user.id
        })

        return JsonResponse({
            "message": "task atualizada",
            "task": serialize_task(task)
        })
    
    elif request.method == "DELETE": 

        delete_task(task)

        logger.info("task_delete_success", extra={
            "user": request.user.username,
            "id": request.user.id
        })

        return JsonResponse({
            "message": "task deletada com sucesso"
        })
    
    logger.warning("task_detail_session_method_not_allowed", extra={
        "method": request.method
    })

    return JsonResponse({
        "error": "método não permitido"
    }, status=405)
