from django.db import models


class WorkSampleMovie(models.Model):
    """
    work_sample_movies
    作品ごとのサンプル動画URL（サイズ別）
    """

    class SizeType(models.IntegerChoices):
        """
        サイズリスト
        """

        SIZE_476_306 = 1, "size_476_306"
        SIZE_560_360 = 2, "size_560_360"
        SIZE_644_414 = 3, "size_644_414"
        SIZE_720_480 = 4, "size_720_480"
        
        @classmethod
        def from_size_type(cls, label):
            return next((v for v, l in cls.choices if l == label), None)


    id = models.BigAutoField(primary_key=True)
    work = models.ForeignKey(
        "Work",
        on_delete=models.CASCADE,
        related_name="sample_movies",
        db_column="work_id",
    )
    url = models.CharField(max_length=1024)
    size_type = models.IntegerField(choices=SizeType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # 1作品に対して「同じサイズ」は1つまで（重複防止）
            models.UniqueConstraint(
                fields=["work", "size_type"],
                name="uniq_work_sample_movie_size",
            ),
            # もし同一サイズでURLが変わる運用があり、履歴を残したいなら↑は外す
        ]
        indexes = [
            models.Index(fields=["work", "size_type"]),
        ]
