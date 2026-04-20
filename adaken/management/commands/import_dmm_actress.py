import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from django.db import transaction

import requests
from django.core.management.base import BaseCommand, CommandError

from adaken.models import Actress


BASE_URL = "https://api.dmm.com/affiliate/v3/ActressSearch"


class Command(BaseCommand):
    help = "Fetch actresses from DMM Affiliate API v3 ActressSearch by initials and export to JSONL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--out", required=False, help="Output JSONL path, e.g. actresses.jsonl"
        )
        parser.add_argument(
            "--initial", required=True, help="Initial chars, e.g. あいうえお or abc..."
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
        # Actress.objects.all().delete()

        if not api_id or not affiliate_id:
            raise CommandError("Env vars DMM_API_ID and DMM_AFFILIATE_ID are required.")

        hits = options["hits"]

        params: Dict[str, Any] = {
            "api_id": api_id,
            "affiliate_id": affiliate_id,
            "initial":options["initial"],
            "hits": hits,
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
            print(result_count)
            # print(result_data["actress"])

            if result_count == 0:
                break

            # ここで保存処理を追加
            actresses = result_data["actress"]

            # 新規登録対象
            to_create = []
            # 上書き対象
            to_update = []

            # dmm_ids = [a.get("id") for a in actresses if a.get("id") is not None]

            for a in actresses:
                print(a)

                dmm_id = a.get("id")
                
                # upsertチェック
                
                
                name = (a.get("name")).strip()
                ruby = (a.get("ruby") or "").strip()  # ある場合

                # 画像URL（返却のキー揺れに対応）
                img = a.get("imageURL") or {}
                if not isinstance(img, dict):
                    img = {}

                image_path_small = img.get("small")
                image_path_lerge = img.get("large")

                birth = a.get("birth")
                bust = a.get("bust")
                cup = a.get("cup")
                waist = a.get("waist")
                hip = a.get("hip")
                height = a.get("height")

                blood_type = a.get("blood_type")
                hobby = a.get("hobby")
                prefectures = a.get("prefectures")

                # 画像URL（返却のキー揺れに対応）
                url_list = a.get("listURL") or {}
                if not isinstance(url_list, dict):
                    url_list = {}

                digital_url = url_list.get("digital")
                monthly_url = url_list.get("monthly")
                mono_url = url_list.get("mono")

                to_create.append(
                    Actress(
                        dmm_id=dmm_id,
                        name=name,
                        ruby=ruby,
                        image_path_small=image_path_small,
                        image_path_lerge=image_path_lerge,
                        birth=birth,
                        height=height,
                        bust=bust,
                        cup=cup,
                        waist=waist,
                        hip=hip,
                        blood_type=blood_type,
                        hobby=hobby,
                        prefectures=prefectures,
                        digital_url=digital_url,
                        monthly_url=monthly_url,
                        mono_url=mono_url,
                        is_active=True,
                    )
                )

            with transaction.atomic():
                if to_create:
                    Actress.objects.bulk_create(to_create, batch_size=500)

            offset += hits
            print(offset)
