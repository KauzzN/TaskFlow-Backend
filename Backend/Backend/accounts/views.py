from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Método não permitido"
        }, status=405)
        
    data = json.loads(request.body)
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return JsonResponse({
            "error": "Dados incompletos"
        }, status=400)
        
    user = authenticate(username=email, password=password)
    
    if user is None:
        return JsonResponse({
            "error": "Credenciais inválidas"
        }, status=401)
        
    login(request, user)
    
    return JsonResponse({
        "message": "Login realizado com sucesso",
        "id": user.id,
        "email": user.email
    })
    
@csrf_exempt
def signIn_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Método não permitido"
        }, status=405)
        
    data = json.loads(request.body)
    
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return JsonResponse({
            "error": "Dados incompletos"
        }, status=400)
        
    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "error": "Email já cadastrado"
        }, status=403)
        
    user = User.objects.create_user(username=email, password=password)
    
    return JsonResponse({
        "message": "Conta registrada com sucesso",
        "Id": user.id,
        "email": user.username
    })