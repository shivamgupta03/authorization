# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from .models import GoogleUser
from .models import Credential
import uuid
import requests
import json
import pytz
from datetime import datetime, timedelta


# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def google_install(request):
    state_token = request.GET.get('state')
    code = request.GET.get('code')
    print (state_token)
    print (code)
    if not state_token and not code:
        # prepare the authorize url and redirect them
        credential = Credential.objects.create(state_token=uuid.uuid4().hex)
        google_user = GoogleUser.objects.create(credential_id=credential.id)
        url = '{}?response_type=code&client_id={}&state={}&redirect_uri={}&scope={}'.format(
            settings.GOOGLE_AUTHORIZATION_URL,
            settings.GOOGLE_CLIENT_ID,
            credential.state_token,
            settings.GOOGLE_REDIRECT_URL,
            'https://www.googleapis.com/auth/contacts.readonly',
        )
        print (url)
        return HttpResponseRedirect(url)
    # Fetch access token with code and state
    credential = Credential.objects.get(state_token=state_token)
    google_user = GoogleUser.objects.create(credential_id=credential.id)
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URL,
    }
    response = requests.post(settings.GOOGLE_TOKEN_URL, data)
    response_data = json.loads(response.content)
    print (response_data)
    credential.access_token = response_data['access_token']
    credential.refresh_token = response_data['refresh_token']
    credential.expires = datetime.now(pytz.utc) + timedelta(seconds=response_data['expires_in'])
    credential.authorization_code = code
    credential.save()
    data = {
        'google_user_id': google_user.id,
        'access_token': credential.access_token,
        'refresh_token': credential.refresh_token,
        'refresh_token_link': 'http://localhost:8080/google/refresh_token?id={}'.format(google_user.id),
        'curl_command_for_contacts': "curl -X GET -H 'Authorization: Bearer {}' 'https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses'".format(credential.access_token)
    }
    return JsonResponse(data)

def refresh_token(request):
    google_user = GoogleUser.objects.get(id=request.GET.get('id'))
    credential = google_user.credential
    old_access_token = credential.access_token
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': credential.refresh_token,
        'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
    }
    response = requests.post(settings.GOOGLE_TOKEN_URL, data)
    response_data = json.loads(response.content)
    print (response_data)
    credential.access_token = response_data['access_token']
    credential.expires = datetime.now(pytz.utc) + timedelta(seconds=response_data['expires_in'])
    credential.save()
    data = {
        'google_user_id': google_user.id,
        'old_access_token': old_access_token,
        'access_token': credential.access_token,
        'refresh_token_link': 'http://localhost:8080/google/refresh_token?id={}'.format(google_user.id),
        'curl_command_for_contacts': "curl -X GET -H 'Authorization: Bearer {}' 'https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses'".format(credential.access_token)
    }
    return JsonResponse(data)
