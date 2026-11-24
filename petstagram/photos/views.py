from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoCreateForm, PhotoUpdateForm
from petstagram.photos.models import Photo


# Create your views here.
def show_photo_details(request: HttpRequest, pk: int) -> HttpResponse:
    photo = get_object_or_404(Photo.objects.prefetch_related("likes", "comments", "tagged_pets"), pk=pk)
    likes = photo.likes.all()
    comments = photo.comments.all()
    comment_form = CommentForm()
    liked_by_user = likes.filter(user_id=request.user.id).exists()

    context = {
        "photo": photo,
        "likes": likes,
        "comments": comments,
        "comment_form": comment_form,
        "liked_by_user": liked_by_user
    }
    return render(request, template_name="photos/photo-details-page.html", context=context)


@login_required
def add_photo(request: HttpRequest) -> HttpResponse:
    form = PhotoCreateForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        form.save_m2m()  # needed after commit=False to save many-to-many fields (e.g. tagged pets)
        return redirect("home")

    return render(request, template_name="photos/photo-add-page.html", context={"form": form})


@login_required
def edit_photo(request: HttpRequest, pk: int) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)
    form = PhotoUpdateForm(request.POST or None, request.FILES or None, instance=photo)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("photo-details", pk=pk)

    return render(request, template_name="photos/photo-edit-page.html", context={"form": form})

# uni version: owner only for edit & delete

@login_required
def delete_photo(request: HttpRequest, pk: int) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)

    photo.delete()

    return redirect("home")
