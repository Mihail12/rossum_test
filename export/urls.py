from django.urls import path

from .views import export_view

urlpatterns = [
    path("export/", export_view, name="export_view"),
]
