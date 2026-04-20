from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from adaken.models import Category


CATEGORY_SEEDS = [
    # (id, name, slug, sort_order)
    (Category.COSTUME, "衣装", "costume", 1),
    (Category.PLACE, "場所", "place", 2),
    (Category.SITUATION, "シチュエーション", "situation", 3),
    (Category.PERSON_F, "女優", "person_f", 4),
    (Category.PERSON_M, "男優", "person_m", 5),
    (Category.PLAY, "プレイ", "play", 6),
    (Category.WORK, "作品", "work", 7),
]


class Command(BaseCommand):
    help = "Seed Category. Idempotent."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding categories..."))

        for id, name, slug, sort_order in CATEGORY_SEEDS:
            Category.objects.update_or_create(
                id=id,
                defaults={
                    "name": name,
                    "slug": slug,
                    "sort_order": sort_order,
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("✅ seed_categories completed."))