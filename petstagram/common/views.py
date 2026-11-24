from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404

from pyperclip import copy
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like, Comment
from petstagram.photos.models import Photo


# Create your views here.
class HomePageView(ListView):
    # model = Photo
    template_name = "common/home-page.html"
    context_object_name = "all_photos"
    paginate_by = 1

    def get_queryset(self):
        queryset = Photo.objects.prefetch_related("tagged_pets", "likes")

        query = self.request.GET.get("pet_name")
        if query:
            queryset = queryset.filter(tagged_pets__name__icontains=query)

        return queryset

# uni version: + annotate() for liked_by_user


    def get_context_data(self, **kwargs):
        kwargs.update({
            "comment_form": CommentForm(),
            "search_form": SearchForm(self.request.GET or None),
        })
        return super().get_context_data(**kwargs)


# def home(request: HttpRequest) -> HttpResponse:
#     all_photos = Photo.objects.prefetch_related("tagged_pets", "likes")
#     comment_form = CommentForm()
#     search_form = SearchForm(request.GET or None)
#
#     if search_form.is_valid():
#         query = search_form.cleaned_data["pet_name"]
#         if query:
#             all_photos = all_photos.filter(tagged_pets__name__icontains=query)
#
#     # search_form = SearchForm()
#     # query = request.GET.get("pet_name")
#     # if query:
#     #     all_photos = all_photos.filter(tagged_pets__name__icontains=query)
#
#     paginator = Paginator(all_photos, per_page=1)
#     page = request.GET.get("page")
#
#     try:
#         all_photos = paginator.page(page)
#     except PageNotAnInteger:
#         all_photos = paginator.page(1)
#     except EmptyPage:
#         all_photos = paginator.page(paginator.num_pages)
#
#     context = {
#         "all_photos": all_photos,
#         "comment_form": comment_form,
#         "search_form": search_form,
#     }
#     return render(request, template_name="common/home-page.html", context=context)
#
# # Uni version: with name in the template input element instead of form in the context


@login_required
def like_functionality(request: HttpRequest, photo_id: int) -> HttpResponse:
    # get_object_or_404(Photo, id=photo_id)
    #
    # if Like.objects.filter(to_photo_id=photo_id).exists():
    #     Like.objects.get(to_photo_id=photo_id).delete()
    # else:
    #     like = Like(to_photo_id=photo_id)
    #     like.save()

    like = Like.objects.filter(to_photo_id=photo_id, user=request.user).first()
    if like:
        like.delete()
    else:
        Like.objects.create(to_photo_id=photo_id, user=request.user)  # Uni version

    return redirect(request.META["HTTP_REFERER"] + f"#{photo_id}")


def copy_link_to_clipboard(request: HttpRequest, photo_id: int) -> HttpResponse:
    link = request.META["HTTP_HOST"] + resolve_url("photo-details", photo_id)
    copy(link)
    return redirect(request.META["HTTP_REFERER"] + f"#{photo_id}")


@login_required
@require_POST
def add_comment(request: HttpRequest, photo_id: int) -> HttpResponse:
    photo = get_object_or_404(Photo, id=photo_id)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.to_photo = photo
        comment.user = request.user
        comment.save()

    return redirect(request.META["HTTP_REFERER"] + f"#{photo_id}")
