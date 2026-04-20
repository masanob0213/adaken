# management/commands/import_dmm_initial.py

import csv
import json
import time
import requests
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from adaken.lib.get_date import get_month_ranges

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
        parser.add_argument("--hits", type=int, default=100)
        parser.add_argument("--sleep", type=float, default=0.2)
        parser.add_argument("--outdir", type=str, default="exports")
        parser.add_argument("--service", type=str, default="digital")
        parser.add_argument("--floor", type=str, default="videoa")

        # 任意：2000固定じゃなくしたい場合
        parser.add_argument("--start-year", type=int, default=2000)

        # 任意：最新月だけ等にしたい場合
        parser.add_argument("--only-year", type=int, default=None)
        parser.add_argument("--only-month", type=int, default=None)

    def handle(self, *args, **opts):
        api_id = getattr(settings, "DMM_API_ID", None)
        affiliate_id = getattr(settings, "DMM_AFFILIATE_ID", None)

        if not api_id or not affiliate_id:
            raise RuntimeError("settings.py に DMM_API_ID / DMM_AFFILIATE_ID を設定してください")

        hits = int(opts["hits"])
        sleep_sec = float(opts["sleep"])
        service = opts["service"]
        floor = opts["floor"]
        outdir = Path(opts["outdir"])
        outdir.mkdir(parents=True, exist_ok=True)

        start_year = int(opts["start_year"])
        only_year = opts["only_year"]
        only_month = opts["only_month"]

        month_ranges = get_month_ranges(start_year=start_year)

        # CSVヘッダ固定
        csv_headers = [
            "product_id",
            "content_id",
            "service_code",
            "floor_code",
            "title",
            "date",
            "url",
            "affiliate_url",
            "maker_name",
            "label",
            "series",
            "genre",
        ]

        total_api_items = 0
        total_saved_db = 0

        for m in month_ranges:
            first_s = m["first_day"]  # "YYYY-MM-DDT00:00:00"
            last_s = m["last_day"]    # "YYYY-MM-DDT23:59:59"

            # 年月を抽出（ファイル名 yyyy/mm.* 用）
            year = int(first_s[0:4])
            month = int(first_s[5:7])

            # フィルタ（任意）
            if only_year and year != int(only_year):
                continue
            if only_month and month != int(only_month):
                continue

            # exports/yyyy/mm.csv & exports/yyyy/mm.json
            ydir = outdir / f"{year:04d}"
            ydir.mkdir(parents=True, exist_ok=True)

            json_path = ydir / f"{month:02d}.json"
            csv_path = ydir / f"{month:02d}.csv"

            self.stdout.write(self.style.SUCCESS(f"\n=== {year:04d}/{month:02d} ==="))
            self.stdout.write(self.style.SUCCESS(f"期間: {first_s} -> {last_s}"))
            self.stdout.write(self.style.SUCCESS(f"出力: {json_path} / {csv_path}"))

            # その月のウィンドウ
            w = FetchWindow(
                start=datetime.fromisoformat(first_s).replace(tzinfo=JST),
                end=datetime.fromisoformat(last_s).replace(tzinfo=JST),
            )

            with json_path.open("w", encoding="utf-8") as f_json, csv_path.open(
                "w", encoding="utf-8", newline=""
            ) as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=csv_headers)
                writer.writeheader()

                api_items, saved = self.fetch_window_and_persist(
                    w=w,
                    api_id=api_id,
                    affiliate_id=affiliate_id,
                    service=service,
                    floor=floor,
                    hits=hits,
                    sleep_sec=sleep_sec,
                    f_json=f_json,
                    csv_writer=writer,
                )

            total_api_items += api_items
            total_saved_db += saved

            # 月間のAPI負荷を少し落とす
            time.sleep(sleep_sec)

        self.stdout.write(self.style.SUCCESS(f"\nAPI取得件数 合計: {total_api_items}"))
        self.stdout.write(self.style.SUCCESS(f"DB新規保存件数 合計: {total_saved_db}"))
        self.stdout.write(self.style.SUCCESS("完了"))

    def fetch_window_and_persist(
        self,
        w: FetchWindow,
        api_id: str,
        affiliate_id: str,
        service: str,
        floor: str,
        hits: int,
        sleep_sec: float,
        f_json,
        csv_writer: csv.DictWriter,
    ) -> Tuple[int, int]:
        """
        window期間をページング取得し
        - JSON(実体はJSONL)にRAWを書き出し
        - CSVにフラットを書き出し
        - DBに重複吸収しつつ保存
        """
        offset = 1
        total_items = 0
        total_saved = 0

        # DMMに渡すフォーマット（ISO形式のまま）
        gte_date = w.start.strftime("%Y-%m-%dT%H:%M:%S")
        lte_date = w.end.strftime("%Y-%m-%dT%H:%M:%S")

        while True:
            params = {
                "api_id": api_id,
                "affiliate_id": affiliate_id,
                "site": "FANZA",
                "service": service,
                "floor": floor,
                "output": "json",
                "sort": "date",
                "hits": hits,
                "offset": offset,
                "gte_date": gte_date,
                "lte_date": lte_date,
            }

            res = requests.get(BASE_URL, params=params, timeout=60)
            if res.status_code >= 400:
                self.stdout.write(self.style.ERROR(f"HTTP {res.status_code}: {res.text[:300]}"))
                res.raise_for_status()

            payload = res.json()
            items = safe_get(payload, ["result", "items"], default=[]) or []
            if not items:
                break

            for it in items:
                # JSONファイル（中身はJSONL：1行1JSON）
                f_json.write(json.dumps(it, ensure_ascii=False) + "\n")
                csv_writer.writerow(self.flatten_item_for_csv(it))

            saved = self.save_items_to_db(items)
            total_saved += saved
            total_items += len(items)

            self.stdout.write(f"offset={offset} fetched={len(items)} saved(new)={saved}")

            if len(items) < hits:
                break
            offset += hits
            time.sleep(sleep_sec)

        self.stdout.write(self.style.SUCCESS(f"Window summary: fetched={total_items}, saved(new)={total_saved}"))
        return total_items, total_saved

    def flatten_item_for_csv(self, it: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "product_id": it.get("product_id", ""),
            "content_id": it.get("content_id", ""),
            "service_code": it.get("service_code", ""),
            "floor_code": it.get("floor_code", ""),
            "title": it.get("title", ""),
            "date": it.get("date", ""),
            "url": it.get("URL", "") or it.get("url", ""),
            "affiliate_url": it.get("affiliateURL", "") or it.get("affiliate_url", ""),
            "maker_name": safe_get(it, ["maker", "name"], "") or "",
            "label": safe_get(it, ["label", "name"], "") or "",
            "series": safe_get(it, ["series", "name"], "") or "",
            "genre": self.join_genres(it),
        }

    def join_genres(self, it: Dict[str, Any]) -> str:
        genres = safe_get(it, ["iteminfo", "genre"], default=[]) or []
        names = []
        if isinstance(genres, list):
            for g in genres:
                if isinstance(g, dict) and g.get("name"):
                    names.append(g["name"])
        return " / ".join(names)

    # @transaction.atomic
    # def save_items_to_db(self, items: List[Dict[str, Any]]) -> int:
    #     objs = []
    #     for it in items:
    #         objs.append(
    #             DmmItem(
    #                 service_code=it.get("service_code", "") or "",
    #                 floor_code=it.get("floor_code", "") or "",
    #                 content_id=it.get("content_id", "") or "",
    #                 product_id=it.get("product_id", "") or "",
    #                 title=it.get("title", "") or "",
    #             )
    #         )

    #     before = DmmItem.objects.count()
    #     DmmItem.objects.bulk_create(objs, ignore_conflicts=True)
    #     after = DmmItem.objects.count()
    #     return max(after - before, 0)