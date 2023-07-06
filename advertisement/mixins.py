class UserQuerySetMixin():
    user_field = 'user'
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = self.request.user.pk
        qs = super().get_queryset(*args, **kwargs)
        if not user.is_staff:
            return qs
        return qs.filter(**lookup_data)
