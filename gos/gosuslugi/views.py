import json
from rest_framework import viewsets, permissions, status
from gosuslugi.models import Polzovateli, Uslugi, ZayavkiPolz
from gosuslugi.serializers import PolzovateliSerializer, UslugiSerializer, ZayavkiPolzSerializer, zayavkiFilter, \
    userFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from gos import settings
from django_filters.rest_framework import DjangoFilterBackend
import redis
import uuid
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.utils import timezone

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# Create your views here.
class PolzovateliViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = Polzovateli.objects.all().order_by("id")
    serializer_class = PolzovateliSerializer
    filterset_class = userFilter


class UslugiViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Uslugi.objects.all().order_by('id')
    serializer_class = UslugiSerializer  # Сериализатор для модели


class ZayavkiPolzViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    queryset = ZayavkiPolz.objects.all().order_by("id")
    serializer_class = ZayavkiPolzSerializer
    filterset_class = zayavkiFilter


@api_view(["POST"])
def create_usluga(request):
    body = json.loads(request.body)
    name = body["name"]
    description = body["description"]
    ssid = request.COOKIES.get("session_cookie")
    if ssid is not None:
        user = Polzovateli.objects.get(username=session_storage.get(request.COOKIES.get('session_cookie')).decode())
        if user.manager:
            p = Uslugi.objects.create(name=name, description=description)
            response = Response("{\"status\": \"ok\"}", content_type="json")
            return response
        else:
            return HttpResponse("{\"status\": \"error\", \"error\": \"access denied\"}")
    else:
        return HttpResponse("{\"status\": \"error\", \"error\": \"you have to logIn\"}")


@api_view(["POST"])
def create_zayavka(request):
    body = json.loads(request.body)
    id_user = body["id_user"]
    id_service = body['id_service']
    status = body["status"]
    ssid = request.COOKIES.get("session_cookie")
    if ssid is not None:
        p = ZayavkiPolz.objects.create(id_user=id_user, id_service=id_service, status=status)
        response = Response("{\"status\": \"ok\"}", content_type="json")
        return response
    else:
        return HttpResponse("{\"status\": \"error\", \"error\": \"вы не можете заказать услугу, проверьте введенные "
                            "данные\"}")

@api_view(['POST'])
def InnChange(request, id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ssid = request.COOKIES.get("session_cookie")
        if ssid is not None:
            inn = body["inn"]
            zay_by_id = Polzovateli.objects.get(id=id)
            zay_by_id.inn = inn
            zay_by_id.save()
            return HttpResponse("{\"status\": \"ok\"}")
        else:
            return HttpResponse("{\"status\": \"access denied\"}")


@api_view(['POST'])
def passChange(request, id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ssid = request.COOKIES.get("session_cookie")
        if ssid is not None:
            passport = body["passport"]
            passport_whom = body["passport_whom"]
            passport_code = body["passport_code"]
            passport_data = body["passport_data"]
            zay_by_id = Polzovateli.objects.get(id=id)
            zay_by_id.passport = passport
            zay_by_id.passport_code = passport_code
            zay_by_id.passport_data = passport_data
            zay_by_id.passport_whom = passport_whom
            zay_by_id.save()
            return HttpResponse("{\"status\": \"ok\"}")
        else:
            return HttpResponse("{\"status\": \"access denied\"}")


@api_view(['POST'])
def SnilsChange(request, id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ssid = request.COOKIES.get("session_cookie")
        if ssid is not None:
            snils = body["snils"]
            zay_by_id = Polzovateli.objects.get(id=id)
            zay_by_id.snils = snils
            zay_by_id.save()
            return HttpResponse("{\"status\": \"ok\"}")
        else:
            return HttpResponse("{\"status\": \"access denied\"}")


@api_view(['POST'])
def statusZayChangeUser(request, id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        head = request.headers
        log = head["username"]
        token = head["Authorization"]
        if (log != "undefind") and (token != "undefind"):
            status = body["status"]
            zay_by_id = ZayavkiPolz.objects.get(id=id)
            zay_by_id.status = status
            zay_by_id.save()
            return HttpResponse("{\"status\": \"ok\"}")
        else:
            return HttpResponse("{\"status\": \"access denied\"}")


@api_view(['POST'])
def uslugiChange(request, id):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        ssid = request.COOKIES.get("session_cookie")
        manager = body['manager']
        if ssid is not None and manager:
            name = body["name"]
            description = body["description"]
            uslugi_by_id = Uslugi.objects.get(id=id)
            uslugi_by_id.name = name
            uslugi_by_id.description = description
            uslugi_by_id.save()
            return HttpResponse("{\"status\": \"ok\"}")
        else:
            return HttpResponse("{\"status\": \"access denied\"}")




@api_view(["POST"])
def create_user(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    u = Polzovateli.objects.create_user(username=username, password=password)
    if u is not None:
        return HttpResponse("{\"status\": \"ok\"}", content_type='json')
    else:
        return HttpResponse("{\"status\": \"error\", \"error\": \"user creation failed\"}", content_type='json')


@api_view(["GET"])
def logout(request):
    ssid = request.COOKIES.get("session_cookie")
    if ssid is not None:
        session_storage.delete(ssid)
        return Response(status=status.HTTP_200_OK, data="{\"status\": \"successfully logged out\"}")
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthView(APIView):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            key = str(uuid.uuid4())
            session_storage.set(key, username)
            u = Polzovateli.objects.get(username=username)
            u.last_login = timezone.now()
            u.save()
            response = Response("{\"status\": \"ok\"}", content_type='json')
            response.set_cookie("session_cookie", key)
            return response
        else:
            return Response("{\"status\": \"error\", \"error\": \"login failed\"}")
