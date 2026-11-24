from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView

from petstagram.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from petstagram.accounts.models import Profile


# Create your views here.
UserModel = get_user_model()

class AppUserRegisterView(CreateView):
    model = UserModel  # no need
    form_class = AppUserCreationForm
    template_name = "accounts/register-page.html"
    success_url = settings.LOGIN_URL

    # create_profile & send welcome email signals triggered


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = "accounts/login-page.html"

    # def form_valid(self, form):
    #     super().form_valid(form)
    #     profile_instance, _ = Profile.objects.get_or_create(user=self.request.user)
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_valid(self, form):
    #     response = super().form_valid(form)  # logs the user in, builds the redirect
    #     Profile.objects.get_or_create(user=form.get_user())
    #     return response  # by chat


class AppUserLogoutView(LogoutView):
    pass


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileEditForm
    template_name = "accounts/profile-edit-page.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse("profile-details", kwargs={"pk": self.object.pk})

# uni version: + CheckIsOwnerMixin


class AppUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = "accounts/profile-details-page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_likes_count"] = sum(p.likes.count() for p in self.object.photos.all())
        return context

# uni version: with Profile, .annotate() and .aggregate()


class AppUserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "accounts/profile-delete-page.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user

    # def delete(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     user.delete()
    #     return redirect(self.get_success_url())


# def register(request: HttpRequest) -> HttpResponse:
#     return render(request, template_name="accounts/register-page.html")

# def login(request: HttpRequest) -> HttpResponse:
#     return render(request, template_name="accounts/login-page.html")

# def show_profile_details(request: HttpRequest, pk: int) -> HttpResponse:
#     return render(request, template_name="accounts/profile-details-page.html")

# def edit_profile(request: HttpRequest, pk: int) -> HttpResponse:
#     return render(request, template_name="accounts/profile-edit-page.html")

# def delete_profile(request: HttpRequest, pk: int) -> HttpResponse:
#     return render(request, template_name="accounts/profile-delete-page.html")
