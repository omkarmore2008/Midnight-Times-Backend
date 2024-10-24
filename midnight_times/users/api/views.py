import os
from datetime import timedelta

import requests
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from midnight_times.users.models import Keyword
from midnight_times.users.models import SearchResult
from midnight_times.users.models import User

from .serializers import SearchKeywordSerializer
from .serializers import UserSerializer, SearchKeywordSerializer

NEWS_API_KEY = os.getenv("NEWS_API_KEY", None)


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ArticleSearchAPIView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchKeywordSerializer

    @extend_schema(request=SearchKeywordSerializer)
    @action(detail=False, methods=["post"])
    def search(self, request):
        request_data = request.data.copy()
        keyword = request_data.get("keyword", "Shree Ram")
        url = f"https://newsapi.org/v2/everything?q={keyword}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        instance, created = Keyword.objects.get_or_create(keyword=keyword, user=request.user)
        threshold_time = timezone.now() - instance.searched_at
        if not created:
            if threshold_time >= timedelta(minutes=15):
                result = SearchResult.objects.get(keyword=instance).articles_list
                return Response(result, status=status.HTTP_200_OK)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            SearchResult.objects.get_or_create(keyword=instance, articles_list=data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
