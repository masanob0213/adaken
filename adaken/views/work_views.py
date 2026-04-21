# adaken/views/work_views.py

from django.utils.dateparse import parse_date
from rest_framework import viewsets

from adaken.models import Work
from adaken.serializers.work_serializers import WorkSerializer


class WorkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkSerializer

    def get_queryset(self):
        queryset = (
            Work.objects.all()
            .select_related("maker")
            .order_by("-id")
        )

        params = self.request.query_params

        # -----------------------------
        # title検索
        # 例: /api/works/?title=サンプル
        # -----------------------------
        title = params.get("title")
        if title:
            queryset = queryset.filter(name__icontains=title)

        # # -----------------------------
        # # メーカー絞り込み
        # # 例: /api/works/?maker_id=1
        # # -----------------------------
        # maker_id = params.get("maker_id")
        # if maker_id:
        #     queryset = queryset.filter(maker_id=maker_id)

        # -----------------------------
        # ジャンル絞り込み
        # 例:
        # /api/works/?major_genre_id=10
        # /api/works/?medium_genre_id=100
        #
        # Work ← WorkGenre → MajorGenre / MediumGenre
        # のような中間テーブルを想定
        # -----------------------------
        major_genre_id = params.get("major_genre_id")
        if major_genre_id:
            queryset = queryset.filter(
                workgenre__major_genre_id=major_genre_id
            )

        # medium_genre_id = params.get("medium_genre_id")
        # if medium_genre_id:
        #     queryset = queryset.filter(
        #         workgenre__medium_genre_id=medium_genre_id
        #     )

        # # -----------------------------
        # # 発売日範囲
        # # 例:
        # # /api/works/?sale_date_from=2026-01-01&sale_date_to=2026-12-31
        # # -----------------------------
        # sale_date_from = params.get("sale_date_from")
        # if sale_date_from:
        #     parsed_from = parse_date(sale_date_from)
        #     if parsed_from:
        #         queryset = queryset.filter(sale_date__date__gte=parsed_from)

        # sale_date_to = params.get("sale_date_to")
        # if sale_date_to:
        #     parsed_to = parse_date(sale_date_to)
        #     if parsed_to:
        #         queryset = queryset.filter(sale_date__date__lte=parsed_to)

        # # -----------------------------
        # # 並び順
        # # 例:
        # # /api/works/?ordering=id
        # # /api/works/?ordering=-id
        # # /api/works/?ordering=sale_date
        # # /api/works/?ordering=-sale_date
        # #
        # # 許可する項目だけに制限
        # # -----------------------------
        # ordering = params.get("ordering")
        # allowed_ordering_fields = {
        #     "id",
        #     "-id",
        #     "sale_date",
        #     "-sale_date",
        #     "title",
        #     "-title",
        # }
        # if ordering in allowed_ordering_fields:
        #     queryset = queryset.order_by(ordering)

        # # JOINで重複しうるため distinct
        # queryset = queryset.distinct()

        # -----------------------------
        # 取得件数制限
        # 例:
        # /api/works/?limit=20
        # 最大100件まで
        # -----------------------------
        limit = params.get("limit")
        if limit:
            try:
                limit = int(limit)
                if limit > 0:
                    limit = min(limit, 100)
                    queryset = queryset[:limit]
            except ValueError:
                pass

        return queryset