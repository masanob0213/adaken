from django.db import models
from django.db.models import Q


class VoteWorkActress(models.Model):
    """
    基本的に素人作品のみに使用される
    actressが登録されていない作品に対して、投票形式で追加してもらう
    """

    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="vote_work_actress_work_relations",
    )

    actress = models.ForeignKey(
        "Actress",
        on_delete=models.CASCADE,
        related_name="vote_work_actress_actress_relations",
    )

    count = models.IntegerField(default=0)
    complete_flg = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "actress"],
                name="uniq_work_actress_director",
            ),
        ]
        indexes = [
            models.Index(fields=["work"]),
            models.Index(fields=["actress"]),
        ]