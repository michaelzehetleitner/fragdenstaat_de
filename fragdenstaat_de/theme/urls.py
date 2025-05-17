from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from froide.urls import (
    admin_urls,
    api_urlpatterns,
    froide_urlpatterns,
    jurisdiction_urls,
)

urlpatterns = [*api_urlpatterns]

urlpatterns += i18n_patterns(
    *froide_urlpatterns,
    *jurisdiction_urls,
    *admin_urls,
    path("", include("cms.urls")),
    prefix_default_language=False,
)
