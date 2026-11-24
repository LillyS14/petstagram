from django.urls import path, include

from . import views


urlpatterns = (
    # path("register/", views.register, name="register"),
    path("register/", views.AppUserRegisterView.as_view(), name="register"),
    # path("login/", views.login, name="login"),
    path("login/", views.AppUserLoginView.as_view(), name="login"),
    path("logout/", views.AppUserLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", include([
        # path("", views.show_profile_details, name="profile-details"),
        path("", views.AppUserDetailView.as_view(), name="profile-details"),
        # path("edit/", views.edit_profile, name="profile-edit"),
        path("edit/", views.ProfileEditView.as_view(), name="profile-edit"),
        # path("delete/", views.delete_profile, name="profile-delete"),
        path("delete/", views.AppUserDeleteView.as_view(), name="profile-delete"),
    ])),
)
