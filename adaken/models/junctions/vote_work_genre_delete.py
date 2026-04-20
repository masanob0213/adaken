from django.db import models
from django.db.models import Q


class VoteWorkGenreDelete(models.Model):
    """
    匿名投票（count集計）
    - medium=NULL の大ジャンル削除提案も許可
    - major削除（medium=NULL）が確定したら、major行＋配下medium行を全削除（ルール2）
    """

    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="genre_delete_vote_relations",
    )
    major_genre = models.ForeignKey(
        "MajorGenre",
        on_delete=models.CASCADE,
        related_name="work_delete_vote_relations",
    )
    medium_genre = models.ForeignKey(
        "MediumGenre",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="work_delete_vote_relations",
    )
    count = models.IntegerField(default=0)
    complete_flg = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "major_genre"],
                condition=Q(medium_genre__isnull=True),
                name="uniq_delvote_work_major_when_medium_null",
            ),
            models.UniqueConstraint(
                fields=["work", "medium_genre"],
                condition=Q(medium_genre__isnull=False),
                name="uniq_delvote_work_medium_when_medium_not_null",
            ),
        ]
        indexes = [
            models.Index(fields=["complete_flg", "count"]),
            models.Index(fields=["work"]),
            models.Index(fields=["major_genre"]),
            models.Index(fields=["medium_genre"]),
        ]

    def save(self, *args, **kwargs):
        if self.medium_genre_id:
            self.major_genre_id = self.medium_genre.major_genre_id
        super().save(*args, **kwargs)