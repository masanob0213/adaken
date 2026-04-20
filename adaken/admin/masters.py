# your_app/admin/masters.py
from django.contrib import admin

from adaken.models import (
    Office,
    Actress,
    Maker,
    Label,
    Series,
    Category,
    MajorGenre,
    MediumGenre,
    DmmGenre,
)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)


@admin.register(Actress)
class ActressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "dmm_id",
        "name",
        "other_name",
        "office",
        "birth",
        "debut_year",
        "is_active",
        "updated_at",
    )
    search_fields = ("dmm_id", "name", "other_name")
    list_filter = ("is_active", "office", "debut_year")
    date_hierarchy = "birth"
    autocomplete_fields = ("office",)
    ordering = ("name",)


@admin.register(Maker)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ruby", "is_active", "updated_at")
    search_fields = ("name", "alias")
    list_filter = ("is_active",)
    ordering = ("name",)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ruby", "maker", "is_active", "updated_at")
    search_fields = ("name", "ruby", "maker")
    list_filter = ("is_active", "maker")
    autocomplete_fields = ("maker",)
    ordering = ("maker__name", "name")


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "dmm_id", "name", "ruby", "label", "is_active", "updated_at")
    search_fields = (
        "dmm_id",
        "name",
        "ruby",
    )
    list_filter = ("is_active", "label")
    autocomplete_fields = ("label",)
    ordering = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "sort_order", "is_active", "updated_at")
    search_fields = ("name", "slug")
    list_filter = ("is_active",)
    ordering = ("sort_order", "name")


@admin.register(MajorGenre)
class MajorGenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "dmm_id",
        "category",
        "is_must_medium",
        "sort_order",
        "is_active",
        "updated_at",
    )
    search_fields = ("dmm_id", "name", "category__name", "category__slug")
    list_filter = ("category", "is_must_medium", "is_active")
    autocomplete_fields = ("category",)
    ordering = ("category__sort_order", "sort_order", "name")


@admin.register(MediumGenre)
class MediumGenreAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "dmm_id",
        "major_genre",
        "sort_order",
        "is_active",
        "updated_at",
    )
    search_fields = (
        "name",
        "dmm_id",
        "major_genre__name",
        "major_genre__category__name",
    )
    list_filter = ("major_genre", "is_active")
    autocomplete_fields = ("major_genre",)
    ordering = ("major_genre__sort_order", "sort_order", "name")


@admin.register(DmmGenre)
class DmmGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ruby", "is_exist_genre", "updated_at")
    search_fields = (
        "id",
        "name",
        "ruby",
        "list_url_dmm",
        "is_exist_genre",
        "updated_at",
    )
