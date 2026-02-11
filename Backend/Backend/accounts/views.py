import jwt
import secrets
import hashlib
import json
import uuid
from datetime import datetime, timedelta

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import RefreshToken
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

def generate_refresh_token(user):
    raw_token = secrets.token_urlsafe(64)

    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    expires_at = timezone.now() + timedelta(days=7)

    RefreshToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at
    )

    return raw_token

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
def refresh_token_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "método não permitido"
        }, status=405)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except(UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "json inválido"
        }, status=400)
    
    incomming_token = data.get("refresh_token")

    if not incomming_token:
        return JsonResponse({
            "error": "refresh_token é obrigatorio"
        }, status=400)
    
    token_hash = hashlib.sha256(incomming_token.encode()).hexdigest()
    
    try:
        refresh = RefreshToken.objects.get(token_hash=token_hash)
    except RefreshToken.DoesNotExist:
        return JsonResponse({
            "error": "refresh token inválido"
        }, status=401)
    
    if refresh.is_expiret():
        refresh.delete()
        return JsonResponse({
            "error": "refresh token expirado"
        }, status=401)
    
    user = refresh.user

    new_refresh_token = generate_refresh_token(user)

    new_access_token = generate_jwt_token(user)

    refresh.delete()

    return JsonResponse({
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }, status=200)

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

    refresh_token = generate_refresh_token(user)
    
    return JsonResponse({
        "message": "Login realizado com sucesso",
        "token": token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "username": user.username
        }
    })

@csrf_exempt
def logout_view(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "método não permitido"
        }, status=405)

    if not request.content_type.startswith("application/json"):
        return JsonResponse({
            "error": "content_type deve ser application/json"
        }, status=400)
    
    try:
        data = json.loads(request.body.decode("utf-8"))
    except(UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({
            "error": "json inválido"
        }, status=400)
    
    incomming_token = data.get("refresh_token")

    if not incomming_token:
        return JsonResponse({
            "error": "refresh token é obrigatorio"
        }, status=401)
    
    token_hash = hashlib.sha256(incomming_token.encode()).hexdigest()
    
    try:
        refresh = RefreshToken.objects.get(token_hash=token_hash)
    except RefreshToken.DoesNotExist:
        return JsonResponse({
            "error": "refresh token inválido"
        }, status=401)
    
    refresh.delete()

    return JsonResponse({
        "message": "logout bem sucedido"
    }, status=200)

    
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
        "message": "Usuário autenticado",
        "id": user.id,
        "username": user.username,
        "email": user.email
    })