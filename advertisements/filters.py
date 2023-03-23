from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from advertisements.models import Advertisement, AdvertisementStatusChoices

class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    creator = SearchFilter()
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    class Meta:
        model = Advertisement
        fields = ['created_at','creator','status']

