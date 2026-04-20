from django.db import models


class Actress(models.Model):
    # 取得サイト別にIDを作成する。
    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    ruby = models.CharField(max_length=255, blank=True, null=True)
    other_name = models.CharField(max_length=255, blank=True, null=True)

    image_path_small = models.CharField(max_length=500, blank=True, null=True)
    image_path_lerge = models.CharField(max_length=500, blank=True, null=True)
    explanation = models.TextField(blank=True, null=True)
    office = models.ForeignKey(
        "Office",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="actresses",
    )

    birth = models.DateField(blank=True, null=True)
    bust = models.FloatField(blank=True, null=True)
    cup = models.CharField(max_length=100, blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hip = models.FloatField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)

    blood_type = models.CharField(max_length=20, null=True, blank=True)
    hobby = models.CharField(max_length=255, null=True, blank=True)
    prefectures = models.CharField(max_length=100, null=True, blank=True)

    debut_year = models.DateField(blank=True, null=True)
    
    # すぐに使用する予定はないが、念の為保存しておく
    digital_url = models.CharField(max_length=500, blank=True, null=True)
    monthly_url = models.CharField(max_length=500, blank=True, null=True)
    mono_url = models.CharField(max_length=500, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["cup"]),
            models.Index(fields=["hip"]),
            models.Index(fields=["height"]),
        ]

    def __str__(self):
        return self.name
