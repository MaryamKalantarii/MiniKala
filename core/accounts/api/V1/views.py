from rest_framework.generics import GenericAPIView
from .serializer import RegistrationSerializer,ResendEmailSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.api.V1.tasks import send_email_with_celery
from accounts.models import CustomeUser
from rest_framework_simplejwt.tokens import AccessToken


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
           
            send_email_with_celery.delay("email/email.html", token, "maryam@admin.com", [user.email])
            
            return Response({"detail": "Email sent. Please check your email."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
class IsVerifiedView(GenericAPIView):
    """
    Handles email verification using a JWT token.

    - Extracts the user ID from the provided token in the URL.
    - Retrieves the corresponding user from the database.
    - Sets the user's `is_verified` flag to True.
    - Returns a success message if verification is successful.
    - Returns an error message if the token is invalid or expired.
    """
    def get(self, request, *args, **kwargs):
        try:
            user_data = AccessToken(kwargs.get("token"))
            user_id = user_data["user_id"]
            user = get_object_or_404(CustomeUser, id=user_id)
            user.is_verified = True
            user.save()
            return Response({"detail": "your account verified successfully"})
        except:
            return Response(
                {
                    "detail": "your token may be expired or changed structure...",
                    "resend email": "http://127.0.0.1:8000/accounts/api/V1/resend",
                }
            )


class ResendEmailView(GenericAPIView):
    """
    Handles resending the verification email to the user.

    - Accepts user email via POST request.
    - Validates the input using a serializer.
    - Checks if the user's email is already verified.
    - If not verified, generates a new access token.
    - Sends a verification email asynchronously using Celery.
    """
    serializer_class = ResendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.is_verified:
            return Response({"detail": "your email is already verified"})
        
        token = self.get_tokens_for_user(user)
        send_email_with_celery.delay("email/email.html", token, "maryam@admin.com", [user.email])
            
        return Response({"detail": "Resend email...!"})

    def get_tokens_for_user(self, user):
        """
        Generates a JWT access token for the given user.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


