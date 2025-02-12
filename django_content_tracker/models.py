from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import gettext_lazy as _

class ContentView(models.Model):
    # Content Object (Generic Relation)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Content Type"))
    object_id = models.PositiveIntegerField(verbose_name=_("Object ID"))
    content_object = GenericForeignKey('content_type', 'object_id')

    # User Information
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='content_views',
        verbose_name=_("User")
    )

    # Device and Browser Information
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_("IP Address"))
    user_agent = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("User Agent"))
    referrer = models.URLField(null=True, blank=True, verbose_name=_("Referrer"))
    device_type = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Device Type"))
    browser = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Browser"))
    os = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Operating System"))

    # Timestamp
    viewed_at = models.DateTimeField(_("Viewed At"), auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.content_object} - {self.viewed_at}"

    class Meta:
        verbose_name = _("Content View")
        verbose_name_plural = _("Content Views")
        ordering = ('-viewed_at',)