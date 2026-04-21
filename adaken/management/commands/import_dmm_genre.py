import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from django.db import transaction

import requests
from django.core.management.base import BaseCommand, CommandError

from adaken.models import MajorGenre
from adaken.models import MediumGenre
from adaken.models import DmmGenre

BASE_URL = "https://api.dmm.com/affiliate/v3/GenreSearch"


class Command(BaseCommand):
    help = "Fetch Genre from DMM Affiliate API v3 GenreSearch by initials and export to JSONL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out", required=False, help="Output JSONL path, e.g. actresses.jsonl"
        )
        parser.add_argument(
            "--initials", default="", help="Initial chars, e.g. あいうえお or abc..."
        )
        parser.add_argument(
            "--hits", type=int, default=100, help="items per request (start with 100)"
        )
        parser.add_argument("--sort", default=None, help="sort key (optional)")
        # parser.add_argument("--keyword", default=None, help="keyword search (optional)")
        parser.add_argument(
            "--max-pages",
            type=int,
            default=0,
            help="0=unlimited, otherwise limit pages per initial",
        )
        parser.add_argument(
            "--sleep", type=float, default=0.3, help="sleep seconds between requests"
        )

    def handle(self, *args, **options):
        api_id = os.getenv("DMM_API_ID")
        affiliate_id = os.getenv("DMM_AFFILIATE_ID")

        # 最終的にはアップサートにする。
        DmmGenre.objects.all().delete()

        if not api_id or not affiliate_id:
            raise CommandError("Env vars DMM_API_ID and DMM_AFFILIATE_ID are required.")

        hits = options["hits"]

        params: Dict[str, Any] = {
            "api_id": api_id,
            "affiliate_id": affiliate_id,
            "floor_id": 43,
            "hits": hits,
            "output": "json",
        }
        DmmGenre.objects.all().delete()
        offset = 1
        result_count = 0
        while True:
            params["offset"] = offset
            r = requests.get(BASE_URL, params=params)
            print(r)

            if r.status_code != 200:
                raise CommandError(
                    f"API request failed. status_code={r.status_code} body={r.text}"
                )

            data = r.json()
            result_data = data["result"]

            result_count = result_data["result_count"]
            # print(result_count)
            # print(result_data["actress"])

            if result_count == 0:
                break

            dmm_genres_to_create = []

            # ここで保存処理を追加
            genres = result_data["genre"]
            for genre in genres:
                print("genre確認")
                # print(genre)
                dmm_id = genre.get("genre_id")
                name = genre.get("name")
                print(dmm_id)
                print(name)

                # medium_genresにNameで一致するレコードが存在するかチェック
                #     存在する場合、対象レコードのdmm_idカラムに、genres.idを登録して処理終了
                medium_genre = MediumGenre.objects.filter(name=name).first()
                if medium_genre:
                    print("ミディ存在")
                    medium_genre.dmm_id = dmm_id
                    medium_genre.save(update_fields=["dmm_id"])
                    continue

                print(medium_genre)

                # major_genresに存在するかチェック
                #     存在する場合、対象レコードのdmm_idカラムに、genres.idを登録して処理終了
                major_genre = MajorGenre.objects.filter(name=name).first()
                if major_genre:
                    print("メジャ存在")
                    major_genre.dmm_id = dmm_id
                    major_genre.save(update_fields=["dmm_id"])
                    continue

                # どちらにも存在しない場合
                #     dmm_genresに登録する。
                dmm_genres_to_create.append(
                    DmmGenre(
                        id=dmm_id,
                        name=name,
                        ruby=genre.get("ruby"),
                        list_url_dmm=genre.get("list_url"),
                    )
                )

            offset += hits
            if dmm_genres_to_create:
                DmmGenre.objects.bulk_create(dmm_genres_to_create)
