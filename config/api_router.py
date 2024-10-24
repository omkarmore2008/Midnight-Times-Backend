from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from midnight_times.users.api.views import UserViewSet, ArticleSearchAPIView

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("", ArticleSearchAPIView, basename="articlesearch")


app_name = "api"
urlpatterns = router.urls
