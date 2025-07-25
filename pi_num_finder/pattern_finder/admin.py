from django.contrib import admin
from .models import PiMil

@admin.register(PiMil)
class PiMilAdmin(admin.ModelAdmin):
    list_display = ('mil_number',)
    search_fields = ('mil_number',)