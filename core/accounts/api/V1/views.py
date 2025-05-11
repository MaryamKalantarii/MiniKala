from rest_framework.generics import GenericAPIView
from .serializer import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_email_with_celery
from accounts.models import CustomeUser

class RegistrationView(GenericAPIView):
    """
    Handles user registration.

    - Accepts user email and password.
    - Validates password and confirms match.
    - Creates a new user upon successful validation.
    - Generates JWT access token.
    - Sends email verification asynchronously using Celery.
    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = get_object_or_404(
                CustomeUser, email=serializer.validated_data["email"]
            )
            token = self.get_tokens_for_user(user)
            send_email_with_celery.delay("email/email.html", token, "admin@hamid.com", [user.email])
            
            return Response({"detail": "if email is on our database email sent for your verification...!"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)