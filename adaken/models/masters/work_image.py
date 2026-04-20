from django.db import models


class WorkImage(models.Model):
    """
    work_images 相当
    - 1作品に複数画像（サンプル画像など）を紐付ける
    """

    class ImageType(models.IntegerChoices):
        """
        サムネイル、サンプルを判別
        """

        IMAGE_URL = 1, "imageURL"  # 作品メイン画像（FANZA: imageURL）
        SAMPLE_IMAGE_URL = 2, "sampleImageURL"  # サンプル画像（FANZA: sampleImageURL）

    class SizeType(models.IntegerChoices):
        """
        画像サイズ
        """

        LIST = 1, "list"
        SMALL = 2, "small"
        LARGE = 3, "large"
        SAMPLE_S = 4, "sample_s"
        SAMPLE_L = 5, "sample_l"

        @classmethod
        def from_size(cls, label):
            return next(v for v, l in cls.choices if l == label)

    id = models.BigAutoField(primary_key=True)
    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="images",
        db_column="work_id",
    )

    sort = models.IntegerField(default=1)
    url = models.CharField(max_length=1024)

    type = models.IntegerField(choices=ImageType.choices)
    size_type = models.IntegerField(choices=SizeType.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # 画像は「作品 + 種別 + サイズ + 並び順」で一意になる想定（必要なら調整）
        constraints = [
            models.UniqueConstraint(
                fields=["work", "type", "size_type", "sort"],
                name="uniq_work_image_type_size_sort",
            ),
        ]
        indexes = [
            models.Index(
                fields=[
                    "work",
                    "type",
                    "size_type",
                ]
            ),
        ]

    def __str__(self) -> str:
        return f"work={self.work_id} type={self.type} size={self.size_type} sort={self.sort}"
