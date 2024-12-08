from rest_framework.filters import SearchFilter as _SearchFilter

from django.db.models import Q


class SearchFilter(_SearchFilter):
    search_param = "search"

    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get(self.search_param, None)
        if not search:
            return queryset
        search_fields = self.get_search_fields(view, request)
        if not search_fields:
            return queryset
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search})
        return queryset.filter(query)
