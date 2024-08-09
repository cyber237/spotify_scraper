from django.db import models


class Podcast(models.Model):

    class Meta:
        verbose_name = "Podcast"
        verbose_name_plural = "Podcasts"
        ordering = ["-added_at"]

    title = models.CharField("Title", max_length=255)
    overall_rating = models.DecimalField(
        "Overall rating", max_digits=2, decimal_places=1
    )
    total_number_of_ratings = models.CharField("Total number of ratings", max_length=6)
    uid = models.CharField("UID", max_length=22, unique=True)
    added_at = models.DateTimeField("Added at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    def __str__(self) -> str:
        return self.title
