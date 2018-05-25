# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from django_filters import DateFromToRangeFilter, CharFilter
from optasks.models import OpsProject


class OpsProjectFilter(filters.FilterSet):
    create_date = DateFromToRangeFilter()
    update_date = DateFromToRangeFilter()
    status = CharFilter(method='status_custom_filter')

    def status_custom_filter(self, queryset, name, value):
        queryset_list = []
        for s in value.split(','):
            queryset_list += queryset.filter(status=s)
        return queryset_list

    class Meta:
        model = OpsProject
        fields = ['pid', 'status', 'demand__id', 'create_date', 'update_date']