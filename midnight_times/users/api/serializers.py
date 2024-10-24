from rest_framework import serializers

from midnight_times.users.models import User, Keyword, SearchResult


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class SearchKeywordSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    name = serializers.CharField(required=False)
    source = serializers.CharField(required=False)
    language  = serializers.CharField(required=False)

