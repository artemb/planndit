from rest_framework import filters


class AccountFilter(filters.DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        account = request.user.account
        if 'account' in queryset.model._meta.get_fields():
            return queryset.filter(account=account)
        else:
            return queryset


class POSTFilter(AccountFilter):
    def filter_queryset(self, request, queryset, view):
        queryset = super(POSTFilter, self).filter_queryset(request, queryset, view)
        if request.method != 'POST':
            return queryset
        filter_class = self.get_filter_class(view, queryset)

        if filter_class:
            return filter_class(request.data, queryset=queryset).qs

        return queryset
