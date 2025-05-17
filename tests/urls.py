from django.urls import include, path

from fragdenstaat_de.theme.urls import urlpatterns as base_urlpatterns

urlpatterns = [
    path("cms/search/", include("fragdenstaat_de.fds_cms.urls", namespace="fds_cms")),
    path(
        "cms/contact/",
        include("fragdenstaat_de.fds_cms.contact", namespace="fds_cms_contact"),
    ),
] + base_urlpatterns
