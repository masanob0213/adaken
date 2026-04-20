from django.db import models
from django.db.models import Q


class WorkGenre(models.Model):
    """
    2行運用
    - 大ジャンル行: medium_genre=NULL
    - 中ジャンル行: medium_genre!=NULL（majorはmediumから自動整合）
    """

    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="genre_relations",
    )

    major_genre = models.ForeignKey(
        "MajorGenre",
        on_delete=models.CASCADE,
        related_name="work_relations",
    )

    medium_genre = models.ForeignKey(
        "MediumGenre",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="work_relations",
    )

    assigned_by = models.CharField(max_length=20, default="admin")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "major_genre"],
                condition=Q(medium_genre__isnull=True),
                name="uniq_workgenre_major_row",
            ),
            models.UniqueConstraint(
                fields=["work", "medium_genre"],
                condition=Q(medium_genre__isnull=False),
                name="uniq_workgenre_medium_row",
            ),
        ]
        indexes = [
            models.Index(fields=["major_genre", "work"]),
            models.Index(fields=["medium_genre", "work"]),
            models.Index(fields=["work"]),
        ]

    def save(self, *args, **kwargs):
        if self.medium_genre_id:
            self.major_genre_id = self.medium_genre.major_genre_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.work_id} - {self.major_genre_id} - {self.medium_genre_id}"