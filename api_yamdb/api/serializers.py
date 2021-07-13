from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserRegistration

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'role', 'first_name', 'last_name', 'bio', 
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = UserRegistration

    def save(self):
        email = self.validated_data['email']
        confirmation_code = get_random_string(length=16)
        UserRegistration.objects.create(
            email=email, confirmation_code=confirmation_code
        )
        send_mail(
            'YaMDb Registration',
            f'Your Confirmation Code: {confirmation_code}',
            'admin@yamdb.org',
            (email,)
        )


class TokenObtainSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    confirmation_code = serializers.CharField(max_length=16, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        confirmation_code = data.get('confirmation_code', None)
        registration_record = get_object_or_404(
            UserRegistration, email=email
        )
        if registration_record.confirmation_code == confirmation_code:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.username = email
                user.save()
            token = RefreshToken.for_user(user)
            return {
                'token': str(token.access_token),
            }
        raise serializers.ValidationError('Wrong Confirmation Code')
