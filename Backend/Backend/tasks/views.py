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
    
    