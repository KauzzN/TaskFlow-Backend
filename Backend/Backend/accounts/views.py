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
    user = data.get("username")
    
    if not email or not password or not user:
        return JsonResponse({
            "error": "Dados incompletos"
        }, status=400)
        
    user = authenticate(username=user, email=email, password=password)
    
    if user is None:
        return JsonResponse({
            "error": "Credenciais inválidas"
        }, status=401)
        
    login(request, user)
    
    return JsonResponse({
        "message": "Login realizado com sucesso",
        "id": user.id,
        "email": user.username
    })
    
@csrf_exempt
def signIn_view(request):
    
    if request.method != "POST":
        return JsonResponse({
            "error": "Método não permitido"
        }, status=405)
        
    if not request.content_type.startswith("application/json"):
        return JsonResponse({
            "error": "Content-type deve ser application/json"
        }, status=400)
        
    try:
        body = request.body.decode("utf-8")
        data = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "Json invalido"    
        }, status=400)


    email = data.get("email")
    password = data.get("password")
    username = data.get("username")
    
    
    if not all([email, password, username]):
        return JsonResponse({
            "error": "Dados incompletos"
        }, status=400)

        
    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "error": "Email já cadastrado"
        }, status=409)
        
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "error": "Usuario já cadastrado"
        }, status=409)
        
        
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    return JsonResponse({
        "message": "Conta registrada com sucesso",
        "Id": user.id,
        "email": user.email,
        "usuario": user.username
    }, status=201)
    
@csrf_exempt
def check_login_view(request):
    
    user = request.user
    
    if request.user.is_authenticated:
        return JsonResponse({
            "message": "Logado",
            "ID": user.id,
            "email": user.username
        })
        
    return JsonResponse({
        "error": "Usuario desconectado"
    }, status=401)
    
@csrf_exempt
def logout_view(request):
    
    user = request.user
    
    if request.user.is_authenticated:
        logout(request)
        
        return JsonResponse({
            "message": "Logout efetuado com sucesso"
        })
        
    return JsonResponse({
        "error": "Usuario não encontrado"
    }, status=401)