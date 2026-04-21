# your_app/admin/junctions.py
from django.contrib import admin

from adaken.models import (
    Work,
    WorkActress,
    WorkGenre,
    VoteWorkGenreAdd,
    VoteWorkGenreDelete,
)


# ==========
# Inlines
# ==========

class WorkActressInline(admin.TabularInline):
    model = WorkActress
    extra = 0
    autocomplete_fields = ("actress",)
    fields = ("actress", "is_main", "sort_order", "created_at")
    readonly_fields = ("created_at",)
    ordering = ("sort_order", "id")


class WorkGenreInline(admin.TabularInline):
    """
    2行運用なので、ここで登録する場合は
    - medium を入れたら major は save() で自動整合される
    - ただし major行（medium=NULL）の自動生成は「サービス層」推奨
      （admin手動運用なら、運用ルールとして major行も追加）
    """
    model = WorkGenre
    extra = 0
    autocomplete_fields = ("major_genre", "medium_genre")
    fields = ("major_genre", "medium_genre", "assigned_by", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("major_genre_id", "medium_genre_id")


class VoteWorkGenreAddInline(admin.TabularInline):
    model = VoteWorkGenreAdd
    extra = 0
    autocomplete_fields = ("major_genre", "medium_genre")
    fields = ("major_genre", "medium_genre", "count", "complete_flg", "completed_at", "updated_at")
    readonly_fields = ("completed_at", "updated_at")
    ordering = ("-count", "-updated_at")


class VoteWorkGenreDeleteInline(admin.TabularInline):
    model = VoteWorkGenreDelete
    extra = 0
    autocomplete_fields = ("major_genre", "medium_genre")
    fields = ("major_genre", "medium_genre", "count", "complete_flg", "completed_at", "updated_at")
    readonly_fields = ("completed_at", "updated_at")
    ordering = ("-count", "-updated_at")


# ==========
# Work admin
# ==========

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "product_number",
        "sale_date",
        "maker",
        "label",
        "series",
        "is_active",
        "updated_at",
    )
    search_fields = (
        "name",
        "product_number",
        "maker_name",
        "label__name",
        "series__name",
    )
    list_filter = (
        "is_active",
        "maker",
        "label",
        "series",
    )
    date_hierarchy = "sale_date"
    autocomplete_fields = ("maker", "label", "series")
    ordering = ("-sale_date", "-updated_at")

    inlines = (
        WorkActressInline,
        WorkGenreInline,
        VoteWorkGenreAddInline,
        VoteWorkGenreDeleteInline,
    )


# ==========
# Junction admins (単体編集も可能にしておく)
# ==========

@admin.register(WorkActress)
class WorkActressAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "actress", "is_main", "sort_order", "created_at")
    search_fields = ("work__name", "work__product_number", "actress__name", "actress__other_name")
    list_filter = ("is_main",)
    autocomplete_fields = ("work", "actress")
    ordering = ("-created_at",)


@admin.register(WorkGenre)
class WorkGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "major_genre", "medium_genre", "assigned_by", "updated_at")
    search_fields = (
        "work__name",
        "work__product_number",
        "major_genre__name",
        "medium_genre__name",
    )
    list_filter = ("assigned_by", "major_genre", "medium_genre")
    autocomplete_fields = ("work", "major_genre", "medium_genre")
    ordering = ("-updated_at",)


@admin.register(VoteWorkGenreAdd)
class VoteWorkGenreAddAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "major_genre", "medium_genre", "count", "complete_flg", "completed_at", "updated_at")
    search_fields = ("work__name", "work__product_number", "major_genre__name", "medium_genre__name")
    list_filter = ("complete_flg", "major_genre")
    autocomplete_fields = ("work", "major_genre", "medium_genre")
    ordering = ("complete_flg", "-count", "-updated_at")


@admin.register(VoteWorkGenreDelete)
class VoteWorkGenreDeleteAdmin(admin.ModelAdmin):
    list_display = ("id", "work", "major_genre", "medium_genre", "count", "complete_flg", "completed_at", "updated_at")
    search_fields = ("work__name", "work__product_number", "major_genre__name", "medium_genre__name")
    list_filter = ("complete_flg", "major_genre")
    autocomplete_fields = ("work", "major_genre", "medium_genre")
    ordering = ("complete_flg", "-count", "-updated_at")