import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.services.auth_service import (
    register_user,
    login_user,
    refresh_session,
    logout_user
)


@csrf_exempt
def login_view(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "método não permitido"}, status=405)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"error": "json inválido"}, status=400)
    
    try:
        
        tokens = login_user(
            data.get("username"),
            data.get("password")
        )
        
        return JsonResponse({
            "success": True,
            "data": tokens
        })
        
    except Exception as e:
        
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=401)
        
        
@csrf_exempt
def refresh_token_view(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "método não permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "json inválido"}, status=400)
    
    try:
        
        tokens = refresh_session(data.get("refresh_token"))
        
        return JsonResponse({
            "success": True,
            "data": tokens
        })
        
    except Exception as e:
        
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=401)
        
        
        
@csrf_exempt
def logout_view(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "método não permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "json inválido"}, status=400)

    logout_user(data.get("refresh_token"))
    
    return JsonResponse({
        "success": True,
        "message": "logout realizado"
    })
    
    
@csrf_exempt
def register_view(request):
    
    if request.method != "POST": 
        return JsonResponse({"error": "método não permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "json inválido"}, status=400)

    try:
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        
        if not username or not email or not password:
            return JsonResponse({
                "error": "campos obrigatorios"
            }, status=400)
            
        result = register_user(username, email, password)
        
        return JsonResponse({
            "success": True,
            "data": result
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)