from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    QuizViewSet, UserAttemptViewSet, UserAnswerViewSet, ResultViewSet,
    RegisterView, CustomTokenObtainPairView, LogoutView, ForgotPasswordView
)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'attempts', UserAttemptViewSet)
router.register(r'answers', UserAnswerViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Authentication APIs
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    # path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Forgot Password API
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
]
