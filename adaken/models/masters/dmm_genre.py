# models.py
from django.db import models


class DmmGenre(models.Model):
    # DMMより取得し、アプリ側のジャンルテーブルに存在しないものを格納
    # アプリ側のジャンルテーブルに保存後、is_exist_genreカラムをtrueにする。

    name = models.CharField(max_length=100)
    ruby = models.CharField(max_length=255, blank=True, null=True)
    list_url_dmm = models.CharField(max_length=500, blank=True, null=True)
    is_exist_genre = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
