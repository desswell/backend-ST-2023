from django_filters import rest_framework as filters
from gosuslugi.models import Polzovateli, Uslugi, ZayavkiPolz
from rest_framework import serializers


class zayavkiFilter(filters.FilterSet):
    id_user = filters.CharFilter()
    id_service = filters.CharFilter()

    class Meta:
        model = ZayavkiPolz
        fields = ['id']


class userFilter(filters.FilterSet):
    username = filters.CharFilter()

    class Meta:
        model = Polzovateli
        fields = ['id']


class PolzovateliSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Polzovateli
        # Поля, которые мы сериализуем
        fields = ["id", "username", "manager", "passport", "fio", "snils", "inn", 'passport_whom', 'passport_code',
                  'passport_data']


class UslugiSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Uslugi
        # Поля, которые мы сериализуем
        fields = ["id", "name", "description"]


class ZayavkiPolzSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = ZayavkiPolz
        # Поля, которые мы сериализуем
        fields = ["id", "id_user", "id_service", "status"]
