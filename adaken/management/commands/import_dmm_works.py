# management/commands/import_dmm_initial.py

import csv
import json
import time
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from django.utils import timezone as dj_timezone

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from adaken.lib.get_date import get_month_ranges
from adaken.models import (
    Work,
    Maker,
    Label,
    Series,
    Director,
    MajorGenre,
    MediumGenre,
    WorkImage,
    WorkSampleMovie,
    WorkGenre,
    WorkActress,
    Actress
)

BASE_URL = "https://api.dmm.com/affiliate/v3/ItemList"
JST = timezone(timedelta(hours=9))


def safe_get(d: Dict[str, Any], path: List[str], default=None):
    cur = d
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return default
        cur = cur[p]
    return cur


@dataclass
class FetchWindow:
    start: datetime
    end: datetime


class Command(BaseCommand):
    help = "DMM作品情報を2000年以降、月ごとに取得し、DB登録＋JSON/CSV保存する"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and validate only, no DB writes",
        )
        # 任意：2000固定じゃなくしたい場合
        parser.add_argument("--only-year", required=True, type=int, default=None)

    def handle(self, *args, **opts):
        ## 検証の場合のみ
        # Label.objects.all().delete()
        # Director.objects.all().delete()
        # WorkImage.objects.all().delete()
        # WorkSampleMovie.objects.all().delete()
        # Work.objects.all().delete()
        api_id = getattr(settings, "DMM_API_ID", None)
        affiliate_id = getattr(settings, "DMM_AFFILIATE_ID", None)

        if not api_id or not affiliate_id:
            raise RuntimeError(
                "settings.py に DMM_API_ID / DMM_AFFILIATE_ID を設定してください"
            )

        # # hits = int(opts["hits"])
        # hits = 100
        # offset = 1

        params: Dict[str, Any] = {
            "api_id": api_id,
            "affiliate_id": affiliate_id,
            "site": "FANZA",
            "service": "digital",
            "floor_id": 43,  # 44も検索すること
            "floor": "videoa",  # videocも取得のこと
            "hits": 100,
            "output": "json",
            "sort": "date",
        }

        only_year = opts["only_year"]
        if only_year:
            month_ranges = get_month_ranges(start_year=only_year)

            with transaction.atomic():
                for m in month_ranges:
                    first_s = m["first_day"]  # "YYYY-MM-DDT00:00:00"
                    # print("first_s")
                    # print(first_s)
                    last_s = m["last_day"]  # "YYYY-MM-DDT23:59:59"
                    # print("last_s")
                    # print(last_s)

                    start = datetime.fromisoformat(first_s).replace(tzinfo=JST)
                    end = datetime.fromisoformat(last_s).replace(tzinfo=JST)

                    gte_date = start.strftime("%Y-%m-%dT%H:%M:%S")
                    lte_date = end.strftime("%Y-%m-%dT%H:%M:%S")

                    params["gte_date"] = gte_date
                    params["lte_date"] = lte_date

                    offset = 1
                    result_count = 0
                    while True:
                        params["offset"] = offset
                        res = requests.get(BASE_URL, params=params)

                        if res.status_code != 200:
                            print("resエラーのため処理終了")
                            print(res.status_code)
                            print(res.text())
                            return

                        data = res.json()
                        result_data = data["result"]

                        result_count = result_data["result_count"]
                        # print(res.request.url)
                        # print(result_count)

                        if result_count == 0:
                            print("result_count=0のため処理終了")
                            break

                        works = result_data["items"]

                        for work in works:
                            # worksテーブルを保存
                            name = work.get("title")
                            affiliate_url = work.get("affiliateURL")
                            product_number = work.get("content_id")
                            sale_date_str = work.get("date")
                            # print(sale_date_str)
                            sale_date = dj_timezone.make_aware(
                                datetime.strptime(sale_date_str, "%Y-%m-%d %H:%M:%S")
                            )
                            # print("作品名：" + name)
                            # print(sale_date)

                            # 商品詳細情報を取得
                            work_detail = work.get("iteminfo")
                            # print("work_detail")
                            # print(work_detail)

                            # メーカ情報を取得、保存
                            # 作品情報のメーカー情報を取得
                            work_maker = work_detail.get("maker")
                            maker = None
                            if work_maker:
                                work_maker_id = work_maker[0].get("id")
                                maker = Maker.objects.filter(
                                    dmm_id=work_maker_id
                                ).first()
                                if maker == None:
                                    # print("メーカー作成確認")
                                    maker = Maker.objects.create(
                                        dmm_id=work_maker_id,
                                        name=work_maker[0].get("name"),
                                    )

                            # レーベル情報を取得、保存
                            work_label = work_detail.get("label")
                            label = None
                            if work_label:
                                work_label_id = work_label[0].get("id")
                                label = Label.objects.filter(
                                    dmm_id=work_label_id
                                ).first()
                                # print("label取得確認")
                                if label == None:
                                    # print("label作成確認")
                                    label = Label.objects.create(
                                        maker=maker,
                                        dmm_id=work_label_id,
                                        name=work_label[0].get("name"),
                                    )

                            # シリーズ情報を取得、保存
                            work_series = work_detail.get("series")
                            series = None
                            if work_series:
                                work_series_id = work_series[0].get("id")
                                series = Series.objects.filter(
                                    dmm_id=work_series_id
                                ).first()
                                if series == None:
                                    series = Series.objects.create(
                                        label=label,
                                        dmm_id=work_series_id,
                                        name=work_series[0].get("name"),
                                    )

                            # 監督情報を取得、保存
                            work_director = work_detail.get("director")
                            director = None
                            if work_director:
                                work_director_id = work_director[0].get("id")
                                director = Director.objects.filter(
                                    dmm_id=work_director_id
                                ).first()
                                if director == None:
                                    director = Director.objects.create(
                                        dmm_id=work_director_id,
                                        name=work_director[0].get("name"),
                                    )

                            created_work = Work.objects.create(
                                maker=maker,
                                label=label,
                                series=series,
                                director=director,
                                name=name,
                                affiliate_url=affiliate_url,
                                product_number=product_number,
                                sale_date=sale_date,
                                site_type=Work.Site_Type.FANZA,
                            )

                            #下記はworkレコード作成後に実施
                            # サンプル画像、動画の保存
                            # ジャケット、サンプル画像
                            # ジャケット画像
                            work_jacket_images = work.get("imageURL")
                            if isinstance(work_jacket_images, dict):
                                for (
                                    jacket_image_type,
                                    jacket_image_url,
                                ) in work_jacket_images.items():
                                    WorkImage.objects.create(
                                        work=created_work,
                                        url=jacket_image_url,
                                        type=WorkImage.ImageType.IMAGE_URL,
                                        size_type=WorkImage.SizeType.from_size(
                                            jacket_image_type
                                        ),
                                    )

                            # サンプル画像
                            work_sample_images = work.get("sampleImageURL")
                            if isinstance(work_sample_images, dict):
                                sort_no = 1
                                for (
                                    sample_image_type,
                                    sample_value,
                                ) in work_sample_images.items():
                                    for sample_image_url in sample_value["image"]:
                                        WorkImage.objects.create(
                                            work=created_work,
                                            url=sample_image_url,
                                            sort=sort_no,
                                            type=WorkImage.ImageType.SAMPLE_IMAGE_URL,
                                            size_type=WorkImage.SizeType.from_size(
                                                sample_image_type
                                            ),
                                        )
                                        sort_no = sort_no + 1

                            # サンプル動画
                            work_sample_movie = work.get("sampleMovieURL")
                            if isinstance(work_sample_movie, dict):
                                for (
                                    sample_movie_type,
                                    sample_movie_url,
                                ) in work_sample_movie.items():
                                    # print("サンプル動画確認")
                                    # print(sample_movie_type)
                                    size_type = WorkSampleMovie.SizeType.from_size_type(
                                        sample_movie_type
                                    )
                                    # pc_flag、sp_flagは関係ないため、WorkSampleMovie.SizeTypeに存在する場合のみインサート
                                    if size_type:
                                        WorkSampleMovie.objects.create(
                                            work=created_work,
                                            url=sample_movie_url,
                                            size_type=size_type,
                                        )

                            # 中間テーブルの作成
                            # 作品 x 女優
                            work_detail_actress_list = work_detail.get("actress")
                            if isinstance(work_detail_actress_list, list):
                                work_detail_actress_sort_order = 1
                                for work_detail_actress in work_detail_actress_list:
                                    # print("work_detail_actress")
                                    # print(work_detail_actress)
                                    work_detail_actress_dmm_id = (
                                        work_detail_actress.get("id")
                                    )
                                    actress = Actress.objects.filter(
                                        dmm_id=work_detail_actress_dmm_id
                                    ).first()

                                    if actress is None:
                                        # TODO:存在しない場合はactressレコードを追加
                                        print("actressが取得できないため処理終了")
                                        print(work_detail_actress)
                                        print(work_detail_actress_dmm_id)
                                        continue

                                    WorkActress.objects.create(
                                        work=created_work,
                                        actress=actress,
                                        sort_order=work_detail_actress_sort_order,
                                    )
                                    work_detail_actress_sort_order += 1

                            # ジャンル x 作品
                            work_detail_genre_list = work_detail.get("genre")
                            if isinstance(work_detail_genre_list, list):
                                for work_detail_genre in work_detail_genre_list:
                                    work_genre_dmm_id = work_detail_genre.get("id")
                                    if work_genre_dmm_id is None:
                                        # print("work_genre_dmm_idが取得できないため処理終了")
                                        # print(work_detail_genre)
                                        continue

                                    major_genre = MajorGenre.objects.filter(
                                        dmm_id=work_genre_dmm_id
                                    ).first()
                                    medium_genre = None

                                    if major_genre is None:
                                        medium_genre = MediumGenre.objects.filter(
                                            dmm_id=work_genre_dmm_id
                                        ).first()

                                    if major_genre is None and medium_genre is None:
                                        # print("major_genre、medium_genreが取得できないため処理終了")
                                        # print(work_detail_genre)
                                        continue

                                    WorkGenre.objects.create(
                                        work=created_work,
                                        major_genre=(
                                            major_genre
                                            if major_genre
                                            else medium_genre.major_genre
                                        ),
                                        medium_genre=medium_genre,
                                    )

                        offset += result_count
                        # print(offset)
