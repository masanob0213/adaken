from django.db import models


class Category(models.Model):
    COSTUME = 1
    PLACE = 2
    SITUATION = 3
    PERSON_F = 4
    PERSON_M = 5
    PLAY = 6
    WORK = 7

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["sort_order"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name
