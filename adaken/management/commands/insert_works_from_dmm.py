import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from adaken.models import Work, Maker, Label, Series, Actress, WorkActress


def parse_sale_date(value: str) -> Optional[datetime]:
    """
    JSONの date は例: "2004-01-31 10:00:03"
    """
    if not value:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def safe_get(d: dict, *keys, default=None):
    cur: Any = d
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


class Command(BaseCommand):
    help = "Import works from JSONL file (1 line = 1 JSON object)."

    def add_arguments(self, parser):
        parser.add_argument("jsonl_path", type=str, help="Path to JSONL file")
        parser.add_argument("--limit", type=int, default=0, help="Limit lines to import (0 = no limit)")
        parser.add_argument("--dry-run", action="store_true", help="Parse and validate only, no DB writes")
        parser.add_argument(
            "--with-relations",
            action="store_true",
            help="Also create related masters (maker/label/series/actress) and work_actress junctions",
        )

    def handle(self, *args, **options):
        jsonl_path = Path(options["jsonl_path"])
        limit = options["limit"]
        dry_run = options["dry_run"]
        with_relations = options["with_relations"]

        if not jsonl_path.exists():
            raise CommandError(f"File not found: {jsonl_path}")

        created = 0
        updated = 0
        skipped = 0
        errors = 0

        # 速度優先でキャッシュ（name->id）
        manufacturer_cache: dict[str, int] = {}
        label_cache: dict[str, int] = {}
        series_cache: dict[str, int] = {}
        actress_cache: dict[str, int] = {}

        def get_or_create_cached(model, cache: dict[str, int], name: str) -> int:
            name = (name or "").strip()
            if not name:
                return 0
            if name in cache:
                return cache[name]
            obj, _ = model.objects.get_or_create(name=name, defaults={"is_active": True} if "is_active" in [f.name for f in model._meta.fields] else {})
            cache[name] = obj.id
            return obj.id

        self.stdout.write(self.style.NOTICE(f"Import start: {jsonl_path}"))
        self.stdout.write(self.style.NOTICE(f"dry_run={dry_run}, with_relations={with_relations}, limit={limit or 'ALL'}"))

        # 既存Workを一括で引けるなら引く（product_numberキー）
        # ただし巨大ファイルだとメモリを食うので、ここはシンプルに行単位upsert
        line_no = 0

        with jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                line_no += 1
                if limit and line_no > limit:
                    break

                line = line.strip()
                if not line:
                    continue

                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    errors += 1
                    self.stderr.write(self.style.ERROR(f"[line {line_no}] JSON decode error"))
                    continue

                product_number = (data.get("product_id") or data.get("content_id") or "").strip()
                title = (data.get("title") or "").strip()
                sale_date = parse_sale_date(data.get("date") or "")

                if not product_number or not title:
                    skipped += 1
                    continue

                manufacturer_id = None
                label_id = None
                series_id = None

                if with_relations:
                    maker_name = None
                    label_name = None
                    series_name = None

                    maker_list = safe_get(data, "iteminfo", "maker", default=[]) or []
                    label_list = safe_get(data, "iteminfo", "label", default=[]) or []
                    series_list = safe_get(data, "iteminfo", "series", default=[]) or []
                    actress_list = safe_get(data, "iteminfo", "actress", default=[]) or []

                    if maker_list and isinstance(maker_list, list):
                        maker_name = (maker_list[0].get("name") or "").strip()
                    if label_list and isinstance(label_list, list):
                        label_name = (label_list[0].get("name") or "").strip()
                    if series_list and isinstance(series_list, list):
                        series_name = (series_list[0].get("name") or "").strip()

                    if maker_name:
                        manufacturer_id = get_or_create_cached(Maker, manufacturer_cache, maker_name) or None
                    if label_name:
                        label_id = get_or_create_cached(Label, label_cache, label_name) or None
                    if series_name:
                        series_id = get_or_create_cached(Series, series_cache, series_name) or None

                if dry_run:
                    created += 1
                    continue

                try:
                    with transaction.atomic():
                        # Workを upsert
                        obj, is_created = Work.objects.get_or_create(
                            product_number=product_number,
                            defaults={
                                "name": title,
                                "sale_date": sale_date,
                                **({"manufacturer_id": manufacturer_id} if manufacturer_id else {}),
                                **({"label_id": label_id} if label_id else {}),
                                **({"series_id": series_id} if series_id else {}),
                            },
                        )

                        # 既存なら更新（タイトルや日付が更新されるケース対応）
                        if not is_created:
                            dirty = False
                            if obj.name != title:
                                obj.name = title
                                dirty = True
                            if sale_date and obj.sale_date != sale_date:
                                obj.sale_date = sale_date
                                dirty = True
                            if with_relations:
                                if manufacturer_id and obj.manufacturer_id != manufacturer_id:
                                    obj.manufacturer_id = manufacturer_id
                                    dirty = True
                                if label_id and obj.label_id != label_id:
                                    obj.label_id = label_id
                                    dirty = True
                                if series_id and obj.series_id != series_id:
                                    obj.series_id = series_id
                                    dirty = True
                            if dirty:
                                obj.save(update_fields=["name", "sale_date", "manufacturer_id", "label_id", "series_id"])

                        if is_created:
                            created += 1
                        else:
                            updated += 1

                        # Actress / junction（任意）
                        if with_relations:
                            actresses = safe_get(data, "iteminfo", "actress", default=[]) or []
                            if isinstance(actresses, list):
                                for a in actresses:
                                    a_name = (a.get("name") or "").strip()
                                    if not a_name:
                                        continue
                                    actress_id = get_or_create_cached(Actress, actress_cache, a_name) or None
                                    if not actress_id:
                                        continue
                                    WorkActress.objects.get_or_create(
                                        work_id=obj.id,
                                        actress_id=actress_id,
                                        defaults={"sort_order": 0} if "sort_order" in [f.name for f in WorkActress._meta.fields] else {},
                                    )

                except Exception as e:
                    errors += 1
                    self.stderr.write(self.style.ERROR(f"[line {line_no}] error: {e}"))
                    continue

        self.stdout.write(self.style.SUCCESS("Import done"))
        self.stdout.write(f"created={created}, updated={updated}, skipped={skipped}, errors={errors}")