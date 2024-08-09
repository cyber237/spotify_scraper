from rest_framework.exceptions import APIException
from rest_framework.generics import RetrieveAPIView

from .models import Podcast
from .scraper import (
    ErrorWhileExtractingPodcastData,
    ErrorWhileFetchingPodCast,
    PodCastNotFound,
    SpotifyScraper,
)
from .serializers import PodcastSerializer


class PodcastDetailView(RetrieveAPIView):
    """
    Retrieve podcast details.
    """

    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer
    lookup_field = "uid"
    lookup_url_kwarg = "uid"

    def _raise_podcast_error(self, exception: Exception) -> None:
        """
        Get error response.
        """
        if isinstance(exception, PodCastNotFound):
            raise APIException(detail="Podcast not found", code=404)
        if isinstance(exception, ErrorWhileFetchingPodCast):
            raise APIException(detail="Error while fetching podcast", code=500)
        if isinstance(exception, ErrorWhileExtractingPodcastData):
            raise APIException(detail="Error while extracting podcast data", code=500)

    def get_object(self):
        """
        Get the podcast object.
        """
        podcast_uid = self.kwargs.get(self.lookup_url_kwarg)
        podcast = Podcast.objects.filter(uid=podcast_uid).first()
        if podcast is None:
            try:
                podcast_data = SpotifyScraper.get_podcast(podcast_uid)
            except Exception as e:
                self._raise_podcast_error(e)
            serializer = self.serializer_class(
                data={**podcast_data, "uid": podcast_uid}
            )
            serializer.is_valid(raise_exception=True)
            podcast = serializer.save()
        return podcast
