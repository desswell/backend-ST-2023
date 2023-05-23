from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth import models as user_models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, username, password, manager, **extra_fields):
        now = timezone.now()
        user = self.model(
            username=username,
            manager=manager,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        user = self._create_user(username, password, True, **extra_fields)
        user.save(using=self._db)
        return user


# Create your models here.
class Polzovateli(user_models.AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, auto_created=True)
    username = models.CharField(max_length=30, blank=True, unique=True)
    manager = models.IntegerField(blank=True)
    passport = models.IntegerField(blank=True, null=True)
    fio = models.CharField(db_column='FIO', max_length=80, blank=True, null=True)  # Field name made lowercase.
    snils = models.IntegerField(db_column='SNILS', blank=True, null=True)  # Field name made lowercase.
    inn = models.IntegerField(db_column='INN', blank=True, null=True)  # Field name made lowercase.
    passport_whom = models.CharField(db_column='passport_whom', max_length=80, blank=True, null=True)
    passport_code = models.CharField(db_column='passport_code', max_length=80, blank=True, null=True)
    passport_data = models.CharField(db_column='passport_data', max_length=80, blank=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'polzovateli'


class Uslugi(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'uslugi'


class ZayavkiPolz(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    id_user = models.IntegerField()
    id_service = models.IntegerField()
    status = models.CharField(max_length=30, blank=True)

    class Meta:
        managed = True
        db_table = 'zayavki_polz'
