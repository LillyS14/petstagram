from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetForm, PetDeleteForm
from petstagram.pets.models import Pet


# Create your views here.
class PetDetailsView(DetailView):
    queryset = Pet.objects.prefetch_related("photos")
    template_name = "pets/pet-details-page.html"
    slug_url_kwarg = "pet_slug"
    # model = Pet
    # context_object_name = "pet"

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update(
            {"all_photos": self.object.photos.all(),
             "comment_form": CommentForm()
             }
        )
        return super().get_context_data(**kwargs)

# def show_pet_details(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = get_object_or_404(Pet.objects.prefetch_related("photos"), slug=pet_slug)  # Uni version: with Prefetch()
#
#     comment_form = CommentForm()
#
#     context = {
#         "pet": pet,
#         "all_photos": pet.photos.all(),
#         "comment_form": comment_form
#     }
#     return render(request, template_name="pets/pet-details-page.html", context=context)


class AddPetView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet-add-page.html"

    def get_success_url(self) -> str:
        return reverse("profile-details", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        pet = form.save(commit=False)
        pet.user = self.request.user
        pet.save()
        return super().form_valid(form)


# def add_pet(request: HttpRequest) -> HttpResponse:
#     form = PetForm(request.POST or None)
#
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return redirect("profile-details", pk=1)
#
#     return render(request, template_name="pets/pet-add-page.html", context={"form": form})


class EditPetView(UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet-edit-page.html"
    slug_url_kwarg = "pet_slug"

    def get_success_url(self):
        return reverse("pet-details", kwargs={"username": self.kwargs["username"], "pet_slug": self.object.slug})


# def edit_pet(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = get_object_or_404(Pet, slug=pet_slug)
#     form = PetForm(request.POST or None, instance=pet)
#
#     if request.method == "POST" and form.is_valid():
#         pet = form.save()
#         return redirect("pet-details", username, pet.slug)  #N.B!
#
#     return render(request, template_name="pets/pet-edit-page.html", context={"form": form})


class DeletePetView(DeleteView):
    model = Pet
    slug_url_kwarg = "pet_slug"
    template_name = "pets/pet-delete-page.html"
    success_url = reverse_lazy("profile-details", kwargs={"pk": 1})  # TODO

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PetDeleteForm(instance=self.object)
        return context

    # def get_object(self, queryset=None):
    #     return Pet.objects.get(slug=self.kwargs["pet_slug"])

    # def delete(self, request, *args, **kwargs):
    #     pet = self.get_object()
    #     pet.delete()
    #     return redirect(self.success_url)

# def delete_pet(request: HttpRequest, username: str, pet_slug: str) -> HttpResponse:
#     pet = get_object_or_404(Pet, slug=pet_slug)
#     form = PetDeleteForm(instance=pet)
#
#     if request.method == "POST":
#         pet.delete()
#         return redirect("profile-details", pk=1)
#
#     return render(request, template_name="pets/pet-delete-page.html", context={"form": form})
