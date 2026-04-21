from django.db import models


class MoreMediumGenreDmm(models.Model):
    medium_genre = models.ForeignKey(
        "MediumGenre",
        on_delete=models.CASCADE,
        related_name="medium_genre",
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
                fields=["medium_genre", "dmm_id"],
                name="uniq_more_medium_genre_dmm_id",
            )
        ]
