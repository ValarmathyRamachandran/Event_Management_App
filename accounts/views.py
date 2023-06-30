from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics,permissions
from accounts.serializers import  LoginSerializers, RegistrationSerializer
from django.contrib.auth import authenticate, login
from accounts.utils import  get_token


User = get_user_model()

class RegistrationApiView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Api for user registration to add new users
        return: Response with message after successful user registration
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                return Response({'message': "User already exists. Please login.", 'code': 401})
            
            serializer.save()
            user = serializer.data
            user.is_active = True
            
            return Response({'message': "User was registered successfully", 'code': 200, 'data': user})
        except Exception as e:
            return Response({'message': 'Oops! Something went wrong! Please try again later', 'code': 400, 'data': str(e)})

class LoginApiView(generics.GenericAPIView):
    """
    LoginApi is used to Login user who have already registered.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializers

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user=User.objects.get(email=email)
            username = user.username

            # Authenticate using email and password
            user = authenticate(request, username=username, password=password)

            if user is None:
                return Response({'message': 'Invalid email or password', 'code': 401})
            login(request, user)
            token = get_token(user)
            return Response({'message': 'User logged in successfully', 'code': 200,'token':token})

        except Exception as e:
            return Response({'message': 'Invalid credentials', 'code': 401, 'data': str(e)})
        

