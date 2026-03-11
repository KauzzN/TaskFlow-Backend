import hashlib
from datetime import timedelta
from django.utils import timezone
from accounts.models import RefreshToken


def create_refresh_token(user, raw_token):
    
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    expires_at = timezone.now() + timedelta(days=7)
    
    return RefreshToken.objects.create(
        user=user,
        token_hash=token_hash,
        expires_at=expires_at
    )
    
def get_refresh_token(raw_token):
    
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    
    try:
        return RefreshToken.objects.get(token_hash=token_hash)
    except RefreshToken.DoesNotExist:
        return None
    
def revoke_token(token):
    
    token.revoked = True
    token.save()
    
def delete_token(token):
    
    token.delete()