from django.db import models


class Director(models.Model):
    # 取得サイト別にIDを作成する。
    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    ruby = models.CharField(max_length=255, blank=True, null=True)

    # しばらく使用はないと思おうが、念のため持たせておく
    image_path_small = models.CharField(max_length=500, blank=True, null=True)
    image_path_lerge = models.CharField(max_length=500, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
