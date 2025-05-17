from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ThemeConfig(AppConfig):
    name = "fragdenstaat_de.theme"
    verbose_name = _("FragDenStaat")
