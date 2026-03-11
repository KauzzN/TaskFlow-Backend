import secrets
from accounts.utils.jwt_utils import generate_access_token
from accounts.repositories.token_repository import create_refresh_token


def generate_tokens(user):

    access_token = generate_access_token(user)

    refresh_token = secrets.token_urlsafe(64)

    create_refresh_token(user, refresh_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }