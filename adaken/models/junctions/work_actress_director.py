from django.db import models
from django.db.models import Q


class WorkActressDirector(models.Model):
    """
    基本的に素人作品のみに使用される
    actressが登録されていない作品に対して、投票形式で追加してもらう
    """

    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="work_actress_director_work_relations",
    )

    actress = models.ForeignKey(
        "Actress",
        on_delete=models.CASCADE,
        related_name="work_actress_director_actress_relations",
    )

    director = models.ForeignKey(
        "Director",
        on_delete=models.CASCADE,
        related_name="work_actress_director_director_relations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "actress", "director"],
                name="work_actress_director_uniq_work_actress_director",
            ),
        ]
        indexes = [
            models.Index(fields=["work"]),
            models.Index(fields=["actress"]),
            models.Index(fields=["director"]),
        ]
