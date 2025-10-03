import random
import string
from django.core.cache import cache
from typing import Optional

def generate_code(length: int = 6) -> str:
    """Генерирует код из 6 цифр возврощает строку"""
    return (str(''.join(random.choices(string.digits, k=length))))

def set_code_in_redis(email: str, code: str, login_token: str) -> str:
    key = f'verify_code:{email}:{login_token}'
    cache.set(key, code, timeout=60*10)  # перезапишет старый код
    return code

def check_code_in_redis_login(email: str, code: str, login_token: str) -> bool:
    key = f'verify_code:{email}:{login_token}'
    stored_code: Optional[str] = cache.get(key)
    if stored_code == code:
        cache.delete(key)
        return True
    return False

def set_code_in_redis_verify(email: str, code: str) -> str:
    key = f'verify_code:{email}'
    cache.set(key, code, timeout=60*10)
    return code

def check_code_in_redis_verify(email: str, code: str) -> bool:
    key = f'verify_code:{email}'
    stored_code: Optional[str] = cache.get(key)
    if stored_code == code:
        cache.delete(key)
        return True
    return False