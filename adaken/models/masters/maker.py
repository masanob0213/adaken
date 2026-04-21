from django.db import models


class Maker(models.Model):
    # メーカーモデル
    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, unique=False)
    ruby = models.CharField(max_length=255, blank=False, null=True)
    list_url_dmm = models.CharField(max_length=500, blank=False, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name
