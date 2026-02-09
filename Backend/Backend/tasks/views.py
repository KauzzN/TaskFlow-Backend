import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from accounts.decorators import jwt_required
from .models import Task

# Create your views here.

@csrf_exempt
@jwt_required
def create_task_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "metodo não permitido"
        },status=405)
        
    
    if not request.content_type.startswith("application/json"):
        return JsonResponse({
            "error": "content_type deve ser application/json"
        }, status=400)
        
    try:
        data = json.loads(request.body.decode("utf-8"))
        
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "json inválido"
        }, status=400)
        
    title = data.get("title")
    description = data.get("description")
    
    if description is None:
        description = ""
    
    if not title:
        return JsonResponse({
            "error": "titulo não foi enviado"
        }, status=400)
    
    if Task.objects.filter(user=request.user,title=title).exists():
        return JsonResponse({
            "error": "você já possui uma task com esse titulo"
        }, status =409)
        
    task = Task.objects.create(
        user=request.user,
        title=title,
        description=description
    )
    
    return JsonResponse({
        "message": "task criada com sucesso",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at
        }
    },status=201)
    
@csrf_exempt
@jwt_required
def read_task_view(request):
    if request.method != "GET":
        return JsonResponse({
            "error": "método não permitido"
        }, status=405)
        
    task_list = []
        
    for task in Task.objects.filter(user = request.user):
        task_data = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at
        }
        
        task_list.append(task_data)
    return JsonResponse({
        "count": len(task_list),
        "tasks": task_list
        }, status=200)

@csrf_exempt
@jwt_required
def find_task_view(request, task_id):
    if request.method != "GET":
        return JsonResponse({
            "error": "método não permitido"
        }, status=405)

    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({
            "error": "Task não encontrada"
        }, status=404)
    
    return JsonResponse({
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at
        }
    }, status=200)

@csrf_exempt
@jwt_required
def update_task_view(request, task_id):
    print("CHEGOU NA UPDATE VIEW", request.method)
    if request.method != "PATCH":
        return JsonResponse({
            "error": "método não permitido"
        }, status=405)
    
    if "application/json" not in request.content_type:
        return JsonResponse({
            "error": "content_type deve ser application/json"
        }, status=400)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except(UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "json inválido"
        }, status=400)
    
    if not data:
        return JsonResponse({
            "error": "nenhum dado enviado"
        }, status=400)
    
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({
            "error": "task não encontrada"
        }, status=404)
    
    updated = False

    if "title" in data:
        if not isinstance(data["title"], str) or not data["title"].strip():
            return JsonResponse({
                "error": "title inválido"
            }, status=400)
        
        if data["title"] != task.title:
            task.title = data["title"]
            updated = True

    if "description" in data:
        if data["description"] is not None and not isinstance(data["description"], str):
            return JsonResponse({
                "error": "description inválido"
            }, status=400)
        
        if data["description"] != task.description:
            task.description = data["description"] or ""
            updated = True
    
    if "is_done" in data:
        if not isinstance(data["is_done"], bool): 
            return JsonResponse({
                "error": "is_done deve ser boolean"
            }, status=400)
        
        if data["is_done"] != task.is_done:
            task.is_done = data["is_done"]
            updated = True

    if not updated:
        return JsonResponse({
            "message": "nenhuma alteração realizada"
        }, status=200)

    task.save()

    return JsonResponse({
        "message": "Task atualizada com sucesso",
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_done": task.is_done,
            "created_at": task.created_at
        }
    }, status=200)

@csrf_exempt
@jwt_required
def delete_task_view(request, task_id):
    if request.method != "DELETE":
        return JsonResponse({
            "error": "Método não permitido"
        }, status=405)
    
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({
            "error": "task não encontrada"
        }, status=404)
    
    task.delete()

    return JsonResponse({
        "message": "task deletada com sucesso"
    }, status=200)