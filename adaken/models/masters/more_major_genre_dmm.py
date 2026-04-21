from django.db import models


class MoreMajorGenreDmm(models.Model):
    major_genres = models.ForeignKey(
        "MajorGenre",
        on_delete=models.CASCADE,
        related_name="major_genres",
    )

    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["major_genres", "dmm_id"],
                name="uniq_more_major_genre_dmm_id",
            )
        ]
