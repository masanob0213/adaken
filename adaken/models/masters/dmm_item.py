# models.py
from django.db import models

class DmmItem(models.Model):
    service_code = models.CharField(max_length=50)
    floor_code = models.CharField(max_length=50)
    content_id = models.CharField(max_length=100, blank=True, default="")
    product_id = models.CharField(max_length=100, blank=True, default="")

    title = models.CharField(max_length=500, blank=True, default="")
    date = models.DateTimeField(null=True, blank=True)  # APIのdateをパース

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # product_id が入るデータ用（空は重複判定に使いにくいので条件付き推奨）
            models.UniqueConstraint(
                fields=["product_id"],
                name="uniq_dmm_product_id",
            ),
            # 保険：複合ユニーク
            models.UniqueConstraint(
                fields=["service_code", "floor_code", "content_id"],
                name="uniq_dmm_service_floor_content",
            ),
        ]