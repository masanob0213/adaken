from django.db import models


class Work(models.Model):
    class Site_Type(models.IntegerChoices):
        """
        販売サイトタイプ
        """

        FANZA = 1
        MGS = 2

    name = models.CharField(max_length=255)

    maker = models.ForeignKey(
        "Maker",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="maker_work",
    )

    label = models.ForeignKey(
        "Label",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="label_work",
    )

    series = models.ForeignKey(
        "Series",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="series_work",
    )

    director = models.ForeignKey(
        "Director",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="director_work",
    )

    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )
    affiliate_url = models.CharField(max_length=500, blank=False, null=True)

    product_number = models.CharField(max_length=64)
    sale_date = models.DateTimeField(blank=True, null=True)
    site_type = models.CharField(max_length=64, blank=False, null=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["product_number"]),
            models.Index(fields=["sale_date"]),
            models.Index(fields=["maker", "product_number"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name
