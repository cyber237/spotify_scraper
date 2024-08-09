from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Podcast


class PodcastSerializer(serializers.ModelSerializer):

    uid = serializers.CharField(
        validators=[
            UniqueValidator(queryset=Podcast.objects.all()),
        ],
        max_length=22,
        min_length=22,
    )

    class Meta:
        model = Podcast
        exclude = [
            "added_at",
            "updated_at",
        ]
