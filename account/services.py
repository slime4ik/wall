from typing import Tuple, Optional, Dict, Any
import uuid
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_code_to_email
from .utils import generate_code, \
    set_code_in_redis
import logging

logger = logging.getLogger("account")

class UserService:
    
    @staticmethod
    def register_user(validated_data) -> Tuple[Optional[User], Optional[str]]:
        """simple registration username+password"""
        validated_data.pop("password2", None)
        try:
            user = User.objects.create_user(**validated_data)
            return user, None
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def login_user(validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks if 2fa required.
        """
        user = validated_data['user']
        if user.email:
            code = generate_code()
            login_token = str(uuid.uuid4())
            set_code_in_redis(user.email, code, login_token)
            send_code_to_email.apply_async(args=[user.email, code])

            return {
                "login_token": login_token,
                "user_id": str(user.id),
                "email": user.email,
                "message": "2FA required",
                "2fa_required": True,
            }

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        return {
            "tokens": {
                "refresh": str(refresh),
                "access": str(access),
            },
            # "user": user,
            "message": "Logged in",
            "2fa_required": False,
        }