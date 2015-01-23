from django.conf.urls import url, include
from rest_framework import routers
from server.apps.authentication import views

router = routers.DefaultRouter()
router.register(r'login', views.LoginViewSet)
router.register(r'namehistory', views.NameHistoryViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
]
