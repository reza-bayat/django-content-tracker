from django.contrib import admin
from .models import ContentView

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user', 'ip_address', 'viewed_at', 'device_type', 'browser', 'os')
    list_filter = ('content_type', 'device_type', 'browser', 'os', 'viewed_at')
    search_fields = ('content_object__title', 'ip_address', 'user_agent')
    date_hierarchy = 'viewed_at'

    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False    