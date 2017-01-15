import json
import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .utils import Credential


def get_redirect_url(request):
    protocol = "https://" if request.is_secure() else "http://"
    return protocol + request.META.get('HTTP_HOST') + reverse(
        "alexa-auth-response")


class AuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        scope_data = json.dumps({
            "alexa:all": {
                "productID": settings.PRODUCT_ID,
                "productInstanceAttributes": {
                    "deviceSerialNumber": "001"
                }
            }
        })

        params = {
            "client_id": settings.CLIENT_ID,
            "scope": "alexa:all",
            "scope_data": scope_data,
            "response_type": "code",
            "redirect_uri": get_redirect_url(request),
        }

        response = requests.get(settings.AMAZON_OAUTH_URL, params=params)
        return redirect(response.url)


class AuthRedirectView(APIView):
    def get(self, request):
        code = request.query_params.get('code')

        post_data = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": get_redirect_url(request)
        }

        response = requests.post(settings.AMAZON_TOKEN_URL,
                                 data=post_data)

        refresh_token = response.json()['refresh_token']
        Credential().dump({'refresh_token': refresh_token})

        return Response()
