from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType

class ContentTrackingMixin:
    @property
    def daily_views(self):
        today = timezone.now().date()
        content_type = ContentType.objects.get_for_model(self)
        return self.contentview_set.filter(viewed_at__date=today).count()

    @property
    def weekly_views(self):
        start_of_week = timezone.now() - timedelta(days=7)
        content_type = ContentType.objects.get_for_model(self)
        return self.contentview_set.filter(viewed_at__gte=start_of_week).count()

    @property
    def monthly_views(self):
        start_of_month = timezone.now() - timedelta(days=30)
        content_type = ContentType.objects.get_for_model(self)
        return self.contentview_set.filter(viewed_at__gte=start_of_month).count()