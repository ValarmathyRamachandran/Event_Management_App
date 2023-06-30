import base64
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import request
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.baseconv import base64
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from jwt import decode

from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }

class TokenOperation:

    @staticmethod
    def token_encode(token):
        token_string_bytes = token.encode("ascii")

        base64_bytes = base64.b64encode(token_string_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string

    @staticmethod
    def token_decode(token_):
        base64_bytes = token_.encode("ascii")

        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        return sample_string


def get_data(request):
    url_token = request.headers.get('Token')
    if not url_token:
        url_token = request.query_params.get('token')
    token = TokenOperation.token_decode(url_token)
    data = decode(token, settings.SECRET_KEY, 'HS256')
    user_data = data
    return user_data

