import jwt
from django.conf import settings
from django.http import JsonResponse
from functools import wraps
from django.contrib.auth.models import User

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.header.get("Authorization")
        
        if not auth_header:
            return JsonResponse({
                "error": "Token não fornecido"
            }, status=401)
            
        
        try:
            token = auth_header.split("")[1]
            
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            
            user_id = payload.get("user_id")
            
            user = User.objects.get(id=user_id)
            
            request.user = user
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({
                "error": "Token expirado"
            }, status=401)
            
        except (jwt.InvalidTokenError, User.DoesNotExist, IndexError):
            return JsonResponse({
                "error": "Token inválido"
            }, status=401)
            
        return view_func(request, *args, **kwargs)
    
    return wrapper