import json
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


@csrf_exempt
@jwt_required
def tasks_view(request):

    if request.method =="GET":

        tasks = Task.objects.filter(user=request.user)
        task_list = [serialize_task(task) for tas in tasks]

        return JsonResponse({
            "count": len(task_list),
            "tasks": task_list
        })
    
    elif request.method == "POST":
        
        data, error = parse_json_body(request)
        if error:
            return error
        
        title = data.get("title")
        description = data.get("description", "")

        if not title:
            return JsonResponse({
                "error": "titulo obrigatorio"
            }, status=400)
        
        task, duplicate = create_task(request.user, title, description)

        if duplicate:
            return JsonResponse({
                "error": "você ja possui uma task com esse titulo"
            }, status=409)

        return JsonResponse({
            "message": "task criada com sucesso",
            "task": serialize_task(task)
        }, status=201)
    
    return JsonResponse({"error": "método não permitido"}, status=405)


@csrf_exempt
@jwt_required
def task_detail_view(request, task_id):

    task = get_task(request.user, task_id)

    if not task:
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
            return JsonResponse({
                "error": "task não encontrada"
            }, status=404)
        
        updated = update_task(task, data)

        if not updated:
            return JsonResponse({
                "message": "nenhuma alteração realizada"
            })
        
        return JsonResponse({
            "message": "task atualizada",
            "task": serialize_task(task)
        })
    
    elif request.method == "DELETE": 

        delete_task(task)

        return JsonResponse({
            "message": "task deletada com sucesso"
        })
    

    return JsonResponse({
        "error": "método não permitido"
    }, status=405)