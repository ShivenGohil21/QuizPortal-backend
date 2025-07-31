from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Quiz, Question, Option, UserAttempt, UserAnswer, Result
from .serializers import QuizSerializer, UserAttemptSerializer, UserAnswerSerializer, ResultSerializer
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
import random;
from .serializers import QuizSerializer, QuestionSerializer 

# User Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

# Custom Login View (optional, default TokenObtainPairView works too)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'username': self.user.username})
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout View (Blacklist token)
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not name or not email or not new_password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=name, email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found with provided details.'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)


# class QuizViewSet(viewsets.ModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()
        questions = list(quiz.questions.all())  # Get questions
        random.shuffle(questions)  # Shuffle the questions

        quiz_data = QuizSerializer(quiz).data
        quiz_data['questions'] = QuestionSerializer(questions, many=True).data

        return Response(quiz_data)


class UserAttemptViewSet(viewsets.ModelViewSet):
    queryset = UserAttempt.objects.all()
    serializer_class = UserAttemptSerializer

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        attempt = self.get_object()
        attempt.completed_at = timezone.now()
        attempt.save()
        # Basic scoring logic
        correct_answers = 0
        answers = attempt.answers.all()
        for answer in answers:
            if answer.selected_option and answer.selected_option.is_correct:
                correct_answers += 1
        result = Result.objects.create(attempt=attempt, score=correct_answers)
        return Response({'message': 'Quiz submitted successfully', 'score': correct_answers})

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer




