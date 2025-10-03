from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserLoginVefificationSerializer, UserEmailSerializer
from .services import UserService
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import check_code_in_redis_login, generate_code, set_code_in_redis_verify, check_code_in_redis_verify
from .models import User, Bookmark
from django.core.cache import cache
from image.models import Wallpaper
from .tasks import send_code_to_email_verify
from supermaster.decorators import ratelimit # custom ratelimit returns 429
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='20/m', method='POST'), name='post')
class RegisterAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user, error = UserService.register_user(serializer.validated_data)
        if user is None:
            return Response({"detail": error}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail": "Вы успешно зарегистрировались!",
        }, status=status.HTTP_201_CREATED)

@method_decorator(ratelimit(key='ip', rate='5/m', method='POST'), name='post')
class LoginAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        result = UserService.login_user(serializer.validated_data)
        
        # Если 2FA не требуется, возвращаем токены
        if not result.get("2fa_required", True):
            return Response({
                "message": result["message"],
                "tokens": result["tokens"]
            }, status=status.HTTP_200_OK)
        
        return Response(result, status=status.HTTP_200_OK)

@method_decorator(ratelimit(key='ip', rate='3/m', method='POST'), name='post')
class LoginVerificationAPIView(APIView):
    """ Ввод кода из почты, если у пользователя включена 2fa"""
    def post(self, request: Request) -> Response:
        serializer = UserLoginVefificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        login_token = request.data.get("login_token")

        email = request.data.get("email")
        if not login_token or not email:
            return Response(
                {"message": "Время вашей сессии истекло, попробуйте войти снова"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if check_code_in_redis_login(email, serializer.validated_data["code"], login_token): # type: ignore
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            cache.delete(f'verify_code:{email}:{login_token}')

            return Response({
                'message': 'Вход выполнен успешно!',
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(access),
                },
                'user': {
                    'username': user.username
                }
            }, status=status.HTTP_200_OK)
        
        return Response(
            {"message": "Invalid code"},
            status=status.HTTP_400_BAD_REQUEST
        )

@method_decorator(ratelimit(key='ip', rate='30/m', method='GET'), name='get')
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "two_factor_enabled": bool(user.email)
        })

@method_decorator(ratelimit(key='ip', rate='4/m', method='POST'), name='post')
class EnableTwoFactorAuthentivationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        # Check if user has email
        if user.email:
            return Response({"message": "Your account already protected"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = UserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check if email is taken
        if User.objects.filter(email=serializer.validated_data["email"]).exists():
            return Response({"message": "This email is already in use"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        code = generate_code()
        set_code_in_redis_verify(serializer.validated_data["email"], code)
        send_code_to_email_verify.apply_async(args=[user.email, code])
        return Response({"message": "Code successfully sent to email"}, status=status.HTTP_200_OK)

@method_decorator(ratelimit(key='ip', rate='3/m', method='POST'), name='post')
class CheckCodeTwoFactorAuthenticationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLoginVefificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get("email")
        if not email:
            return Response(
                {"message": "Your session time's expired, try again"},
                status=status.HTTP_403_FORBIDDEN
            )

        code = serializer.validated_data["code"]

        # Проверка кода
        if check_code_in_redis_verify(email, code):
            user = request.user
            user.email = email
            user.save()

            return Response(
                {"message": "Two-factor authentication successfully enabled"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Invalid or expired code"},
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(ratelimit(key='ip', rate='30/m', method='POST'), name='post')
class AddToBookmarksAPIView(APIView):
    def post(self, request, wallpaper_id):
        try:
            wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, wallpaper=wallpaper)

            if created:
                return Response({"message": "You successfully bookmarked this wallpaper"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "You already bookmarked this wallpaper"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

@method_decorator(ratelimit(key='ip', rate='30/m', method='DELETE'), name='delete')
class RemoveFromBookmarksAPIView(APIView):
    def delete(self, request, wallpaper_id):
        try:
            wallpaper = get_object_or_404(Wallpaper, id=wallpaper_id)
            deleted, _ = Bookmark.objects.filter(user=request.user, wallpaper=wallpaper).delete()

            if deleted:
                return Response({"message": "Bookmark removed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)