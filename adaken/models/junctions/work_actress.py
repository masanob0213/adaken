from django.db import models


class WorkActress(models.Model):
    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="actress_relations",
    )

    actress = models.ForeignKey(
        "Actress",
        on_delete=models.CASCADE,
        related_name="work_relations",
    )

    # 出演順
    sort_order = models.PositiveIntegerField(default=0)

    # 主演フラグ
    is_main = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["work", "actress"],
                name="uniqu_work_actress",
            )
        ]
        indexes = [
            models.Index(fields=["work", "sort_order"]),
            models.Index(fields=["actress"]),
            models.Index(fields=["is_main"]),
        ]

    def __str__(self):
        return f"{self.work_id} - {self.actress_id}"