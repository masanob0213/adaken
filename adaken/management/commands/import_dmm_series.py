import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from django.db import transaction

import requests
from django.core.management.base import BaseCommand, CommandError

from adaken.models import Series


BASE_URL = "https://api.dmm.com/affiliate/v3/SeriesSearch"


class Command(BaseCommand):
    help = "Fetch actresses from DMM Affiliate API v3 ActressSearch by initials and export to JSONL."

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "--out", required=True, help="Output JSONL path, e.g. actresses.jsonl"
    #     )
    #     parser.add_argument(
    #         "--initials", default="", help="Initial chars, e.g. あいうえお or abc..."
    #     )
    #     parser.add_argument(
    #         "--hits", type=int, default=100, help="items per request (start with 100)"
    #     )
    #     parser.add_argument("--sort", default=None, help="sort key (optional)")
    #     # parser.add_argument("--keyword", default=None, help="keyword search (optional)")
    #     parser.add_argument(
    #         "--max-pages",
    #         type=int,
    #         default=0,
    #         help="0=unlimited, otherwise limit pages per initial",
    #     )
    #     parser.add_argument(
    #         "--sleep", type=float, default=0.3, help="sleep seconds between requests"
    #     )

    def handle(self, *args, **options):
        api_id = os.getenv("DMM_API_ID")
        affiliate_id = os.getenv("DMM_AFFILIATE_ID")
        if not api_id or not affiliate_id:
            raise CommandError("Env vars DMM_API_ID and DMM_AFFILIATE_ID are required.")

        params: Dict[str, Any] = {
            "api_id": api_id,
            "affiliate_id": affiliate_id,
            "floor_id": 43,
            "output": "json",
        }
        offset = 1
        result_count = 0
        while True:
            params["offset"] = offset
            r = requests.get(BASE_URL, params=params)

            if r.status_code != 200:
                break

            data = r.json()
            result_data = data["result"]

            result_count = result_data["result_count"]
            # print(result_data["actress"])

            if result_count == 0:
                break

            # ここで保存処理を追加
            dmm_series_result = result_data["series"]

            # 新規登録対象
            to_create = []

            # dmm_ids = [a.get("id") for a in actresses if a.get("id") is not None]

            for series in dmm_series_result:
                dmm_id = series.get("series_id")
                name = (series.get("name")).strip()
                ruby = (series.get("ruby") or "").strip()  # ある場合
                list_url = (series.get("list_url") or "").strip()

                to_create.append(
                    Series(
                        dmm_id=dmm_id,
                        name=name,
                        ruby=ruby,
                        list_url_dmm=list_url,
                        is_active=True,
                    )
                )

            with transaction.atomic():
                if to_create:
                    Series.objects.bulk_create(to_create, batch_size=500)

            offset += result_count
            print(offset)
