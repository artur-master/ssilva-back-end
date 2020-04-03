from django.urls import path, re_path
from django.conf.urls import include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user-permissions',
                UserProfilePermissionViewSet,
                base_name='user-permissions')
router.register('user-profiles', UserProfileViewSet, base_name='user-profiles')
router.register('user-notifications',
                UserNotificationViewSet,
                base_name='user-notifications')
router.register('role-permissions', RolePermissionViewSet)
router.register('inmobiliarias', InmobiliariaViewSet)
router.register('constructoras', ConstructoraViewSet)
router.register(
    'inmobiliarias-aprobadores',
    AprobadorInmobiliariaViewSet,
    base_name='inmobiliarias-aprobadores')
router.register(
    'inmobiliarias-representantes',
    RepresentanteInmobiliariaViewSet,
    base_name='inmobiliarias-representantes')
router.register('inmobiliarias-users-types', UserInmobiliariaTypeViewSet)
router.register('regiones', RegionViewSet)
router.register('provincias', ProvinciaViewSet)
router.register('comunas', ComunaViewSet)
router.register('permissions', PermissionViewSet)
router.register('contact-info-types', ContactInfoTypeViewSet)
router.register('login', LoginViewSet, base_name='login')
router.register(
    'constants-numerics',
    ConstantNumericViewSet,
    base_name='constants-numerics')


urlpatterns = [
    path(
        '',
        include(
            router.urls)),
    path(
        'password-update/',
        UpdatePasswordAPIView.as_view()),
    path(
        'password-reset/<uuid:user_id>',
        ResetPasswordUserAPIView.as_view()),
    path(
        'user-activate/<uuid:user_id>',
        ActiveDisableUserAPIView.as_view()),
    path(
        'uf/',
        UFNowAPIView.as_view()),
    path(
        'uf-de/',
        UFDeAPIView.as_view()),
    path(
        'uf-simulador/',
        UFSimuladorAPIView.as_view()),
    re_path(
        r'^uf/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$',
        UFAPIView.as_view(),
        name='uf'),
    re_path(
      r'^uf-de/<int:monto>/(?P<date>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$',
        UFDeDateAPIView.as_view(),
      name='uf-de')
]
