from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from requests.auth import HTTPBasicAuth
import json
from db import forms

# POST /rest/api/content
# GET /rest/api/content/{id}
temp_body = ''
def test_yadro(request):
    print('----- test_yadro -----')
    if request.POST:
        form = forms.page_form(request.POST, request.FILES)
        if form.is_valid():
            try:
                command = form.cleaned_data['command']
                id = form.cleaned_data['id']
                user = form.cleaned_data['user']
                password = form.cleaned_data['password']
                space = form.cleaned_data['space']
                title = form.cleaned_data['title']
                body = form.cleaned_data['text']
                print('- command:', command)
                if command == 'create_page':
                    url = 'http://192.168.0.208:8000/confluence/' # /rest/api/content
                    auth = HTTPBasicAuth(user, password)
                    headers = {'Accept': 'application/json',
                               'Content-Type': 'application/json'}
                    data = {
                        'type': 'page',
                        'title': title,
                        'ancestors': [{'id': None}],
                        'space': {'key': space},
                        'body': {
                            'storage': {
                                'value': body,
                                'representation': 'storage',
                            }
                        }
                    }
                    try:
                        response = requests.post(url,
                                                 auth=auth,
                                                 headers=headers,
                                                 data=data
                                                 ).json()
                    except Exception as err:
                        print("- create_page requests.post exception:", err)
                    # print('id', response['id'])
                    if response['id'] != '':
                        return HttpResponse(response['id'])
                    else:
                        return HttpResponse(False)
                if command == 'get_page' and id:
                    # print('Запрос', user, password, id)
                    url = 'http://192.168.0.208:8000/confluence/'  # /rest/api/content/{id}
                    auth = HTTPBasicAuth(user, password)
                    headers = {'Accept': 'application/json',
                               'Content-Type': 'application/json'}
                    params = dict(id=id, expand=None, status=None, version=None)
                    try:
                        response = requests.get(url,
                                                auth=auth,
                                                headers=headers,
                                                params=params
                                                ).json()
                    except Exception as err:
                        print("- get_page requests.get exception:", err)
                    print('keys:', list(response.keys()))
                    space = response['space']['key']
                    title = response['title']
                    body = response['body']['storage']['value']
                    # print(text)
                    return HttpResponse(json.dumps(dict(space=space, title=title, body=body)))
            except Exception as err:
                print("- test_yadro exception:", err)
                return HttpResponse(False)
    else:
        return render(request, 'db/test_yadro.html')

@csrf_exempt
def confluence_server_imitation(request):
    print('----- confluence_server_imitation -----', request.method)
    if request.method == "POST":
        return HttpResponse(json.dumps({'id': '45'}, ensure_ascii=False))
    if request.method == "GET":
        print('- request:', request.GET)
        page_data = {
            'id': request.GET['id'],
            'type': 'page',
            'title': 'title',
            'ancestors': [{'id': None}],
            'space': {'key': 'space'},
            'body': {
                'storage': {
                    'value': '<p>' + 'Текст страницы ' + str(request.GET['id']) + '<p>',
                    'representation': 'storage',
                }
            }
        }
        print('- HttpResponse -')
        return HttpResponse(json.dumps(page_data, ensure_ascii=False))