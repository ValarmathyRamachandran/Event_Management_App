from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',
            'is_admin',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm Password do not match."
            )

        validate_password(password)  # Validate password against Django's default validators

        return attrs
    
    def create(self, validated_data):
        """
        Create and save a new User instance.
        Args:validated_data (dict): Validated data containing the user attributes.
        Returns: The created User instance.

        """
        password = validated_data.pop('password') 
        user = User(**validated_data) 
        user.set_password(password) #This method takes care of hashing the password for security purposes.
        user.save()
        return user


class LoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    class Meta:
        model = User
        fields = ['username', 'password']
        required_fields = fields

    


class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email'
        ]

