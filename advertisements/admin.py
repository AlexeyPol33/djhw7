from django.contrib import admin
from .models import Advertisement, AdvertisementStatusChoices

# Register your models here.
@admin.register(Advertisement)
class AdminAdvertisement(admin.ModelAdmin):
    list_display = [
        'title',
        'description',
        'status',
        'creator',
        'created_at',
        'updated_at',
    ]
    pass
