from django.db import models


class MajorGenre(models.Model):
    # =========================
    # COSTUME（衣装系）
    # =========================
    COSTUME_SEIFUKU = 101
    COSTUME_COSPLAY = 102
    COSTUME_EXPOSURE = 103
    COSTUME_SWIMSUIT = 104
    COSTUME_UNDERWEAR = 105
    COSTUME_PANTYHOSE = 106
    COSTUME_WAFUKU = 107
    COSTUME_SPORTS = 108
    COSTUME_MINISKIRT = 109

    # =========================
    # PLACE（場所）
    # =========================
    PLACE_HOME = 201
    PLACE_SCHOOL = 202
    PLACE_HOTEL = 203
    PLACE_RYOKAN = 204
    PLACE_OFFICE = 205
    PLACE_CAR_SEX = 206
    PLACE_SEA = 207
    PLACE_ONSEN = 208
    PLACE_HOSPITAL = 209
    PLACE_POOL = 210
    PLACE_FITTING_ROOM = 211
    PLACE_PREVIEW_ROOM = 212
    PLACE_OUTDOOR = 213

    # =========================
    # SITUATION（シチュエーション）
    # =========================
    SITUATION_RELATION = 301
    SITUATION_SCENE = 302
    SITUATION_FUZOKU = 303
    SITUATION_JOB = 304
    SITUATION_NTR = 305

    # =========================
    # PERSON（女優）
    # =========================
    PERSON_STYLE = 401
    PERSON_BREAST = 402
    PERSON_HIP = 403
    PERSON_LEG = 404
    PERSON_TYPE = 405
    PERSON_PERSONALITY = 406
    PERSON_HAIR_STYLE = 407
    PERSON_HAIR_COLOR = 408
    PERSON_VOICE = 409

    # =========================
    # PERSON（男優）
    # =========================
    PERSON_M_STYLE = 501
    PERSON_M_TYPE = 502

    # =========================
    # PLAY（プレイ）
    # =========================
    PLAY_SEIJOUI = 601
    PLAY_KIJOUI = 602
    PLAY_BACK = 603
    PLAY_FELLATIO = 604
    PLAY_HANDJOB = 605
    PLAY_SQUIRT = 606
    PLAY_LOTION = 607
    PLAY_MULTI = 608
    PLAY_MULTI_F1 = 609
    PLAY_MULTI_M1 = 610
    PLAY_MULTI_MULTI = 611
    PLAY_FINISH = 612
    PLAY_RAPE = 613
    PLAY_DRUG = 614
    PLAY_FOREPLAY = 615
    PLAY_DEBUT = 616
    PLAY_HARD = 617
    PLAY_TOY = 618
    PLAY_FETISH = 619
    PLAY_HAMEDORI = 620
    PLAY_SWEATY = 621
    PLAY_SHUKAN = 622
    PLAY_ONANIE = 623
    PLAY_ITAZURA = 624
    PLAY_LES = 625
    PLAY_SOKUHAME = 626

    # =========================
    # WORK（作品）
    # =========================
    WORK_FAN_APPRECIATION = 701
    WORK_ORIGINAL_COLLAB = 702
    WORK_8K_VR = 703
    WORK_4K = 704
    WORK_ACTRESS_BEST = 705
    WORK_16H_OVER = 706
    WORK_HIGH_QUALITY_VR = 707
    WORK_COLLAB = 708
    WORK_REPRINT = 709
    WORK_4H_OVER = 710
    WORK_DEBUT = 711
    WORK_BEST = 712
    WORK_SOLO = 713

    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="major_genres",
    )

    dmm_id = models.BigIntegerField(
        unique=True,
        db_index=True,
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=100)
    ruby = models.CharField(max_length=255, blank=True, null=True)
    list_url_dmm = models.CharField(max_length=500, blank=True, null=True)

    is_must_medium = models.BooleanField(default=False)

    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="uniq_major_genre_category_name",
            )
        ]
        indexes = [
            models.Index(fields=["category", "sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"
