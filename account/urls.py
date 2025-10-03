from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LoginVerificationAPIView, AddToBookmarksAPIView, RemoveFromBookmarksAPIView,\
    ProfileAPIView,EnableTwoFactorAuthentivationAPIView, CheckCodeTwoFactorAuthenticationAPIView

urlpatterns = [
    path('registration/', RegisterAPIView.as_view(), name='registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('login-verification/', LoginVerificationAPIView.as_view(), name='login-verification'),
    path('bookmark/<int:wallpaper_id>/', AddToBookmarksAPIView.as_view(), name='add_bookmark'),
    path('bookmark/<int:wallpaper_id>/remove/', RemoveFromBookmarksAPIView.as_view(), name='remove_bookmark'),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("2fa/enable/", EnableTwoFactorAuthentivationAPIView.as_view(), name="enable-2fa"),
    path("2fa/verify/", CheckCodeTwoFactorAuthenticationAPIView.as_view(), name="verify-2fa"),
]