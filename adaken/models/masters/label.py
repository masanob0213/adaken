from django.db import models


class Label(models.Model):
    # メーカーモデル

    # シリーズはレーベル不明もあり得るので NULL 可（必要なら必須化）
    maker = models.ForeignKey(
        "Maker",
        on_delete=models.SET_NULL,
        null=True,
        related_name="Maker",
    )

    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, unique=False)
    ruby = models.CharField(max_length=255, blank=False, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
