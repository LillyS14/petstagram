from django.urls import path, include
from .views import add_photo, show_photo_details, edit_photo, delete_photo

urlpatterns = (
    path("add/", add_photo, name="photo-add"),
    path("profile/<int:pk>/", include([
        path("", show_photo_details, name="photo-details"),
        path("edit/", edit_photo, name="photo-edit"),
        path("delete/", delete_photo, name="photo-delete"),
    ])),
)
