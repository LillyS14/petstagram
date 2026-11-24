from django.urls import path, include
from . import views

urlpatterns = (
    path("add/", views.AddPetView.as_view(), name="pet-add"),
    path("<str:username>/pet/<slug:pet_slug>/", include([
        path("", views.PetDetailsView.as_view(), name="pet-details"),
        path("edit/", views.EditPetView.as_view(), name="pet-edit"),
        path("delete/", views.DeletePetView.as_view(), name="pet-delete"),
    ])),
)

# urlpatterns = (
#     path("add/", views.add_pet, name="pet-add"),
#     path("<str:username>/pet/<slug:pet_slug>/", include([
#         path("", views.show_pet_details, name="pet-details"),
#         path("edit/", views.edit_pet, name="pet-edit"),
#         path("delete/", views.delete_pet, name="pet-delete"),
#     ])),
# )
