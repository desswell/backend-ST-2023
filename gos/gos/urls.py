from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from gosuslugi import views as gosuslugi_views


router = routers.DefaultRouter()
router.register(r'polzovateli', gosuslugi_views.PolzovateliViewSet)
router.register(r'uslugi', gosuslugi_views.UslugiViewSet)
router.register(r'zayavkipolz', gosuslugi_views.ZayavkiPolzViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/addUsl', gosuslugi_views.create_usluga),
    path('api/addZay', gosuslugi_views.create_zayavka),
    path('api/uslugiCh/<int:id>', gosuslugi_views.uslugiChange),
    path('api/statusZayChUser/<int:id>', gosuslugi_views.statusZayChangeUser),
    path('api/user/create', gosuslugi_views.create_user, name="create-user"),
    path('api/logout', gosuslugi_views.logout, name="logout"),
    path('api/authorize', gosuslugi_views.AuthView.as_view(), name="auth"),
    path('api/innCh/<int:id>', gosuslugi_views.InnChange),
    path('api/snilsCh/<int:id>', gosuslugi_views.SnilsChange),
    path('api/passCh/<int:id>', gosuslugi_views.passChange),
]
