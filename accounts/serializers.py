from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=50, min_length=8,style={'input_type': 'password'}, write_only=True)
    default_error_messages = {'username': 'Username should contains only alphanumeric characters'}

    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password','confirm_password','is_admin']
        extra_kwargs = {'password': {'write_only': True}}
        required_fields = ['first_name','last_name','email','password','confirm_password']

    
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)

        if not username.isalnum() or password != confirm_password:
            raise serializers.ValidationError('Invalid username or passwords do not match.')  
        return attrs
    
    def create(self, validated_data):
        """
        Create and save a new User instance.
        Args:validated_data (dict): Validated data containing the user attributes.
        Returns: The created User instance.

        """
        password = validated_data.get('password') 
        #hashed_password = make_password(password)
        user = User.objects.create_user(**validated_data) 
        return user


class LoginSerializers(serializers.ModelSerializer):
     email = serializers.EmailField()
     password = serializers.CharField(style={'input_type': 'password'})

     class Meta:
        model = User
        fields = ['email', 'password']
        required_fields = fields
        

    
class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email'
        ]

