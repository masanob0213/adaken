import json
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from django.db import transaction

import requests
from django.core.management.base import BaseCommand, CommandError

from adaken.models import Series



class Command(BaseCommand):
    help = "Fetch actresses from DMM Affiliate API v3 ActressSearch by initials and export to JSONL."

    def handle(self, *args, **options):
            # 新規登録対象
            to_create_major = []
            to_create_midium = []

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
