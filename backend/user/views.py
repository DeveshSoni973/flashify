from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# Register View: Handles user registration
class RegisterView(APIView):
    def post(self, request):
        # Validate and serialize data
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save new user
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View: Handles user login and JWT token generation
class LoginView(APIView):
    def post(self, request):
        # Validate login data with LoginSerializer
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Authenticate user
            user = authenticate(username=username, password=password) #we decoted the AUTH_MODEL in settings.py
            if user is not None:
                # Generate JWT token
                token = RefreshToken.for_user(user)
                
                # Serialize user data (without password)
                user_data = UserSerializer(user).data
                
                # Return token and user data
                return Response({
                    'access': str(token.access_token),
                    'refresh': str(token),
                    'user': user_data
                }, status=status.HTTP_200_OK)
            
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout View: Handles user logout by blacklisting the refresh token
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Blacklist the refresh token to log out the user
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
            return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



