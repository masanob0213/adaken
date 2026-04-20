from django.contrib import admin
# your_app/admin.py
from .admin.masters import *  # noqa
from .admin.junctions import *  # noqa

# Register your models here.
