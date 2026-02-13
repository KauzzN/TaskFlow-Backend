import jwt
import json
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def generate_jwt_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    
    return token

def get_user_from_token(request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(" ")[1]
        
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        
        user_id = payload.get("user_id")
        return User.objects.get(id=user_id)
    
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None

@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "Método não permitido"
        }, status=405)
    
    if not request.content_type.startswith("application/json"):
        return JsonResponse({
            "error": "Content-type deve ser application/json"
        }, status=400)
        
    try:
        data = json.loads(request.body.decode("utf-8"))
    except(UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "Json inválido"
        }, status=400)
    
    password = data.get("password")
    username = data.get("username")
    
    if not all([password, username]):
        return JsonResponse({
            "error": "Dados incompletos"
        }, status=400)
        
    user = authenticate(username=username, password=password)
    
    if user is None:
        return JsonResponse({
            "error": "Credenciais inválidas"
        }, status=401)
        
    token = generate_jwt_token(user)
    
    return JsonResponse({
        "message": "Login realizado com sucesso",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username
        }
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
        data = json.loads(request.body.decode("utf_8"))
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
    
    token = generate_jwt_token(user)
    
    return JsonResponse({
        "message": "Conta criada com sucesso",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }, status=201)
    
@csrf_exempt
def check_login_view(request):
    
    user = get_user_from_token(request)
    
    if not user:
        return JsonResponse({
            "error": "Credenciais inválidas"
        }, status=401)
        
    return JsonResponse({
        "message": "Usuário autenticado com sucesso",
        "id": user.id,
        "username": user.username,
        "email": user.email
    })
    