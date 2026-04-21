from django.db import models


class MediumGenre(models.Model):
    # =========================
    # 衣装 > 制服
    # =========================
    COSTUME_SEIFUKU_SAILOR = 101
    COSTUME_SEIFUKU_BLAZER = 102

    # =========================
    # 衣装 > コスプレ
    # =========================
    COSTUME_COSPLAY_NURSE = 103
    COSTUME_COSPLAY_NERSE = 103  # 互換
    COSTUME_COSPLAY_MAID = 104
    COSTUME_COSPLAY_MEID = 104  # 互換
    COSTUME_COSPLAY_CHINA = 105
    COSTUME_COSPLAY_BONDAGE = 106
    COSTUME_COSPLAY_BODYCON = 107
    COSTUME_COSPLAY_MINISKIRT_POLICE = 108
    COSTUME_COSPLAY_BUNNY = 109
    COSTUME_COSPLAY_SUIT_OL = 110
    COSTUME_COSPLAY_CHEER = 143
    COSTUME_COSPLAY_CAT = 144
    COSTUME_COSPLAY_NAKED_APRON = 145

    # =========================
    # 衣装 > 露出状態
    # =========================
    COSTUME_EXPOSURE_ALL = 111
    COSTUME_EXPOSURE_HALF = 112
    COSTUME_EXPOSURE_OPEN = 113
    COSTUME_EXPOSURE_SEE_THROUGH = 114

    # =========================
    # 衣装 > 水着
    # =========================
    COSTUME_SWIM_NORMAL = 115
    COSTUME_SWIM_BIKINI = 116
    COSTUME_SWIM_SCHOOL = 117

    # =========================
    # 衣装 > 下着
    # =========================
    COSTUME_UNDER_BRA = 118
    COSTUME_UNDER_TBACK = 119
    COSTUME_UNDER_LINGERIE = 120
    COSTUME_UNDER_GARTER = 121
    COSTUME_UNDER_SPORTS = 122
    COSTUME_UNDER_NO_BRA = 123
    COSTUME_UNDER_NO_PANTIES = 124
    COSTUME_UNDER_PANTY_FLASH = 125

    # =========================
    # 衣装 > パンスト
    # =========================
    COSTUME_PANTY_TIGHTS = 126
    COSTUME_PANTY_STOCKING = 127
    COSTUME_PANTY_KNEE = 128
    COSTUME_PANTY_LOOSE = 129
    COSTUME_PANTY_KNEE_SOX = 142

    # =========================
    # 衣装 > 和服・浴衣
    # =========================
    COSTUME_WAFUKU_YUKATA = 130
    COSTUME_WAFUKU_KIMONO = 131
    COSTUME_WAFUKU_COS = 132

    # =========================
    # 衣装 > スポーツ
    # =========================
    COSTUME_SPORT_GYM = 133
    COSTUME_SPORT_VOLLEY = 134
    COSTUME_SPORT_TENNIS = 135
    COSTUME_SPORT_BICYCLE = 136

    # =========================
    # 場所
    # =========================
    PLACE_HOME_BED = 201
    PLACE_HOME_LIVING = 202
    PLACE_HOME_BATH = 203
    PLACE_HOME_KITCHEN = 204

    PLACE_SCHOOL_CLASS = 205
    PLACE_SCHOOL_GYM = 206
    PLACE_SCHOOL_POOL = 207

    PLACE_HOTEL_LUXURY = 208
    PLACE_HOTEL_LOVE = 209

    PLACE_POOL_SCHOOL = 210
    PLACE_POOL_NIGHT = 211
    PLACE_POOL_PRIVATE = 212

    # =========================
    # シチュエーション > 関係性
    # =========================
    SITUATION_RELATION_COUPLE = 301
    SITUATION_RELATION_MARRIED = 302
    SITUATION_RELATION_COLLEAGUE = 303
    SITUATION_RELATION_CLASSMATE = 304
    SITUATION_RELATION_AFFAIR = 305
    SITUATION_RELATION_NTR = 306
    SITUATION_RELATION_FEMALE_BOSS = 307
    SITUATION_RELATION_MALE_BOSS = 308
    SITUATION_RELATION_BRIDE = 309
    SITUATION_RELATION_CHILDHOOD = 310
    SITUATION_RELATION_DAUGHTER = 311
    SITUATION_RELATION_CLUB_MANAGER = 312
    SITUATION_RELATION_SUBORDINATE = 313
    SITUATION_RELATION_INCEST = 314
    SITUATION_RELATION_IN_LAW = 354

    # =========================
    # シチュエーション > シーン
    # =========================
    SITUATION_SCENE_WORK = 315
    SITUATION_SCENE_DATE = 316
    SITUATION_SCENE_NANPA = 317
    SITUATION_SCENE_GYAKUNAN = 318
    SITUATION_SCENE_GOUKON = 319
    SITUATION_SCENE_PRIVATE = 320
    SITUATION_SCENE_AMATEUR = 321
    SITUATION_SCENE_TRAVEL = 322
    SITUATION_SCENE_MASSAGE = 323
    SITUATION_SCENE_PEEPING = 324

    # =========================
    # シチュエーション > 風俗
    # =========================
    SITUATION_FUZOKU_MENESU = 325
    SITUATION_FUZOKU_PINSARO = 326
    SITUATION_FUZOKU_CABARET = 327
    SITUATION_FUZOKU_SEX_CABARET = 328
    SITUATION_FUZOKU_GIRLSBAR = 329
    SITUATION_FUZOKU_HEALTH_SOAP = 330

    # =========================
    # シチュエーション > 職業
    # =========================
    SITUATION_JOB_WIFE = 331
    SITUATION_JOB_HOUSEWIFE = 332
    SITUATION_JOB_SECRETARY = 333
    SITUATION_JOB_BEAUTICIAN = 334
    SITUATION_JOB_TEACHER = 335
    SITUATION_JOB_TUTOR =3236
    SITUATION_JOB_ATHLETE = 337
    SITUATION_JOB_RECEPTIONIST = 338
    SITUATION_JOB_INVESTIGATOR = 339
    SITUATION_JOB_CABARET_GIRL = 340
    SITUATION_JOB_COLLEGE_GIRL = 341
    SITUATION_JOB_SCHOOL_GIRL = 342
    SITUATION_JOB_MATURE_WOMAN = 343
    SITUATION_JOB_NURSE = 344
    SITUATION_JOB_BUS_GUIDE = 345
    SITUATION_JOB_RACE_QUEEN = 346
    SITUATION_JOB_MODEL = 347
    SITUATION_JOB_INSTRUCTOR = 348
    SITUATION_JOB_OL = 349
    SITUATION_JOB_GEINOU = 352
    SITUATION_JOB_MIKO = 353
    SITUATION_JOB_PRINCE = 355
    SITUATION_JOB_OKAMI = 356
    SITUATION_JOB_CANGAL = 357
    SITUATION_JOB_CA = 358
    SITUATION_JOB_JOI = 359
    SITUATION_JOB_ANNOUNCER = 360
    SITUATION_JOB_MIBOUJIN= 361
    SITUATION_JOB_WAITRESS = 362
    SITUATION_JOB_COMPANION = 363
    SITUATION_JOB_GOKUDO = 364
    SITUATION_JOB_KUNOICHI = 365
    
    # =========================
    # シチュエーション > 寝取り・寝取られ・NTR
    # =========================
    SITUATION_NTR_TAKER = 350
    SITUATION_NTR_TAKEN = 351

    # =========================
    # 女優 > スタイル
    # =========================
    PERSON_STYLE_SLENDER = 401
    PERSON_STYLE_GLAMOUR = 402
    PERSON_STYLE_SMALL = 403
    PERSON_STYLE_TALL = 404
    PERSON_STYLE_CURVY = 405
    PERSON_STYLE_HAIRLESS = 406
    PERSON_STYLE_TANNED = 407
    PERSON_STYLE_NO_MAKEUP = 408

    # =========================
    # 女優 > 胸
    # =========================
    PERSON_BREAST_BIG = 409
    PERSON_BREAST_BEAUTIFUL = 410
    PERSON_BREAST_SMALL = 411

    # =========================
    # 女優 > お尻
    # =========================
    PERSON_HIP_BEAUTIFUL = 412
    PERSON_HIP_BIG = 413

    # =========================
    # 女優 > 脚
    # =========================
    PERSON_LEG_BEAUTIFUL = 414

    # =========================
    # 女優 > タイプ
    # =========================
    PERSON_TYPE_BISHOUJO = 415
    PERSON_TYPE_SEISO = 416
    PERSON_TYPE_GAL = 417
    PERSON_TYPE_COOL = 418
    PERSON_TYPE_CUTE = 419
    PERSON_TYPE_BOYISH = 420
    PERSON_TYPE_M = 421
    PERSON_TYPE_GLASSES = 422
    PERSON_TYPE_ONEESAN = 423
    PERSON_TYPE_VIRGIN = 424
    PERSON_TYPE_BITCH = 425

    # =========================
    # 女優 > 性格
    # =========================
    PERSON_PERSONALITY_COOL = 424
    PERSON_PERSONALITY_TSUNDERE = 425
    PERSON_PERSONALITY_BRAT = 426
    PERSON_PERSONALITY_CHIJO = 427

    # =========================
    # 女優 > 髪型
    # =========================
    PERSON_HAIR_VERY_LONG = 428
    PERSON_HAIR_LONG = 429
    PERSON_HAIR_SHORT = 430
    PERSON_HAIR_VERY_SHORT = 431
    PERSON_HAIR_BOB = 432
    PERSON_HAIR_PONYTAIL = 433
    PERSON_HAIR_TWINTAIL = 434

    # =========================
    # 女優 > 髪色
    # =========================
    PERSON_HAIR_COLOR_BLACK = 435
    PERSON_HAIR_COLOR_BLONDE = 436
    PERSON_HAIR_COLOR_BROWN = 437

    # =========================
    # 女優 > 声
    # =========================
    PERSON_VOICE_CUTE = 438
    PERSON_VOICE_OHO = 439

    # =========================
    # 男優 > スタイル
    # =========================
    PERSON_M_STYLE_MUSCLE = 501
    PERSON_M_STYLE_CHUBBY = 502
    PERSON_M_STYLE_THIN = 503
    PERSON_M_STYLE_BIG_D = 504

    # =========================
    # 男優 > タイプ
    # =========================
    PERSON_M_TYPE_IKEMEN = 505
    PERSON_M_TYPE_VIRGIN = 506
    PERSON_M_TYPE_GAY = 507
    PERSON_M_TYPE_PE = 508
    PERSON_M_TYPE_M = 509

    # =========================
    # プレイ > バック
    # =========================
    PLAY_BACK_SLEEP = 601
    PLAY_BACK_STAND = 602
    PLAY_BACK_DOGGY = 603

    # =========================
    # プレイ > フェラチオ
    # =========================
    PLAY_FELLATIO_IMA = 604
    PLAY_FELLATIO_JUPO = 605
    PLAY_FELLATIO_PERO = 606
    PLAY_FELLATIO_INSTANT = 607

    # =========================
    # プレイ > コキ
    # =========================
    PLAY_HANDJOB_NORMAL = 608
    PLAY_HANDJOB_FOOT = 609
    PLAY_HANDJOB_TOY = 610
    PLAY_HANDJOB_ARM = 611
    PLAY_HANDJOB_THIGH = 612
    PLAY_HANDJOB_PAIZURI = 613

    # =========================
    # プレイ > 潮吹き
    # =========================
    PLAY_SQUIRT_MASSIVE = 614
    PLAY_SQUIRT_MALE = 615

    # =========================
    # プレイ > ローション・オイル
    # =========================
    PLAY_LOTION_MASSAGE = 616

    # =========================
    # プレイ > 複数
    # =========================
    PLAY_MULTI_3P_4P = 617
    PLAY_MULTI_RANKOU = 618
    PLAY_MULTI_HARLEM = 676

    # =========================
    # プレイ > 複数（女1）
    # =========================
    PLAY_MULTI_F1_3P = 619
    PLAY_MULTI_F1_4P = 620
    PLAY_MULTI_F1_5P = 621

    # =========================
    # プレイ > 複数（男1）
    # =========================
    PLAY_MULTI_M1_3P = 622
    PLAY_MULTI_M1_4P = 623
    PLAY_MULTI_M1_5P = 624

    # =========================
    # プレイ > 複数（多：多）
    # =========================
    PLAY_MULTI_MM_2_2 = 625
    PLAY_MULTI_MM_3_3 = 626
    PLAY_MULTI_MM_4_4 = 627
    PLAY_MULTI_MM_5_5 = 628

    # =========================
    # プレイ > フィニッシュ
    # =========================
    PLAY_FINISH_NAKADASHI = 629
    PLAY_FINISH_GOMU = 630
    PLAY_FINISH_FACIAL = 631
    PLAY_FINISH_BOOBS = 632
    PLAY_FINISH_ASS = 633
    PLAY_FINISH_GOKKUN = 634
    PLAY_FINISH_BUKKAKE = 635
    PLAY_FINISH_MOUSE = 634  # 互換

    # =========================
    # プレイ > 媚薬
    # =========================
    PLAY_DRUG_PILL = 636
    PLAY_DRUG_LOTION = 637
    PLAY_DRUG_TABACCO = 638

    # =========================
    # プレイ > 前戯
    # =========================
    PLAY_FOREPLAY_69 = 639
    PLAY_FOREPLAY_CUNNI = 640
    PLAY_FOREPLAY_FACE_SIT = 641
    PLAY_FOREPLAY_SIX_NINE = 642

    # =========================
    # プレイ > ハードプレイ
    # =========================
    PLAY_HARD_PISTON = 643
    PLAY_HARD_ORGASM = 644
    PLAY_HARD_WHITE_EYES = 645
    PLAY_HARD_SPANKING = 646
    PLAY_HARD_ANAL = 647
    PLAY_HARD_BONDAGE = 648
    PLAY_HARD_ENEMA = 649
    PLAY_HARD_SCAT = 650
    PLAY_HARD_DRUG = 651
    PLAY_HARD_CONFINEMENT = 652
    PLAY_HARD_SM = 653
    PLAY_HARD_PREGNANCY = 654
    PLAY_HARD_KOUSOKU = 655
    PLAY_HARD_HUMILIATION= 667
    PLAY_HARD_CRUEL= 671
    PLAY_HARD_SCATOLOGY= 674
    PLAY_HARD_ANAL= 675
    PLAY_HARD_VERBAL_ABUSE= 677

    # =========================
    # プレイ > おもちゃ
    # =========================
    PLAY_TOY_DILDO = 656
    PLAY_TOY_DENMA = 657
    PLAY_TOY_ROTOR = 658
    PLAY_TOY_VIBE = 676

    # =========================
    # プレイ > フェチ
    # =========================
    PLAY_FETISH_SWAPPING = 659
    PLAY_FETISH_MILK = 660
    PLAY_FETISH_DIRTY_TALK = 661
    PLAY_FETISH_URINE_DRINK = 662
    PLAY_FETISH_URINATION = 663
    PLAY_FETISH_SHOTA = 664
    PLAY_FETISH_ASS = 665
    PLAY_FETISH_LEG = 666
    PLAY_FETISH_FUTANARI= 668
    PLAY_FETISH_TENTACLE_PLAY= 669
    PLAY_FETISH_BOYS_LOVE= 670
    PLAY_FETISH_CROSSDRESSING= 671
    PLAY_FETISH_TRANS_WOMAN= 673
    

    # =========================
    # プレイ > レズ
    # =========================
    PLAY_LES_SISTERS = 667

    major_genre = models.ForeignKey(
        "MajorGenre",
        on_delete=models.CASCADE,
        related_name="medium_genres",
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

    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["major_genre", "name"],
                name="uniq_medium_genre_major_name",
            )
        ]
        indexes = [
            models.Index(fields=["major_genre", "sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.major_genre.name} - {self.name}"
