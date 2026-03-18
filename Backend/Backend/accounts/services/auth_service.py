import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.services.token_service import generate_tokens
from accounts.repositories.token_repository import (
    get_refresh_token,
    revoke_token,
    delete_token
)


logger = logging.getLogger(__name__)

def register_user(username, email, password):
    
    if User.objects.filter(username=username).exists():
        raise Exception("username já existe")
    
    if User.objects.filter(email=email).exists():
        raise Exception("email já cadastrado")
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    
    tokens = generate_tokens(user)
    
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        },
        "tokens": tokens
    }


def login_user(username, password):

    user = authenticate(username=username, password=password)
    
    logger.info("login_user_authenticated", extra={
    "user": username
    })

    if not user:
        logger.warning("login_invalid_credentials")

        raise Exception("credenciais inválidas")
    
        
    return generate_tokens(user)


def refresh_session(refresh_token):
    
    token = get_refresh_token(refresh_token)
    
    if not token:
        raise Exception("refresh token inválido")
    
    if token.revoked or token.is_expired():
        delete_token(token)
        raise Exception("refresh token inválido")
    
    user = token.user
    
    revoke_token(token)
    
    return generate_tokens(user)


def logout_user(refresh_token):
    
    token = get_refresh_token(refresh_token)
    
    if not token:
        return
    
    revoke_token(token)
