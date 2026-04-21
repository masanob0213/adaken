from django.db import models


class Series(models.Model):
    # シリーズはレーベル不明もあり得るので NULL 可（必要なら必須化）
    label = models.ForeignKey(
        "Label",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="series",
    )
    
    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=255)
    ruby = models.CharField(max_length=255, blank=True, null=True)
    list_url_dmm = models.CharField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["label"]),
        ]

    def __str__(self):
        return self.name
