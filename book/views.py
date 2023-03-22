from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book, Review
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE
from django.views import generic
# from .forms import CreateBookForm
import os
# Create your views here.


class ListBookView(LoginRequiredMixin, ListView):
    template_name = "book/book_list.html"
    # htmlファイルで↓のモデルの中身が使いまわされる
    model = Book
    paginate_by = ITEM_PER_PAGE


class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = "book/book_detail.html"
    model = Book


class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = "book/book_create.html"
    model = Book
    fields = {"title", "text", "category", "thumbnail"}
    success_url = reverse_lazy("index")
    # form_class = CreateBookForm

    def form_valid(self, form):
        # ユーザー情報の追加をする関数
        form.instance.user = self.request.user

        """ save_path = str("media/"+self.request.FILES['picture'])
        up_data = self.request.FILES['picture']
        with open(save_path, 'wb+') as i:
            for chunk in up_data.chunks():
                i.write(chunk)
        with PIL.Image.open(save_path) as image:
            os.remove(save_path)

            # 画像の縦横比をそのままに480×640以下にリサイズ
            resized_height = 640 / int(image.size[0]) * image.size[1]
            resized_image = image.resize((640, int(resized_height)))
            if resized_height > 480:
                resized_width = 480 / int(image.size[1]) * image.size[0]
                resized_image = resized_image.resize((int(resized_width), 480))

            image_io = io.BytesIO()
            resized_image.save(image_io, format="JPEG")
            image_file = InMemoryUploadedFile(image_io, field_name=None, name=save_path,
                                              content_type="image/jpeg", size=image_io.getbuffer().nbytes,
                                              charset=None)

        post = form.save(commit=False)
        post.picture = image_file
        post.save() """

        return super().form_valid(form)


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "book/book_delete.html"
    model = Book
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj


class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = "book/book_update.html"
    model = Book
    fields = {"title", "text", "category", "thumbnail"}
    # success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied

        return obj

    def get_success_url(self):
        return reverse("detail-book", kwargs={"pk": self.object.id})


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "book/review_form.html"
    model = Review
    fields = {"book", "title", "text", "rate"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.get(pk=self.kwargs["book_id"])
        # print(context)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("detail-book", kwargs={"pk": self.object.book.id})


def index_view(request):
    # print("index_view is called")
    object_list = Book.objects.order_by("-id")
    # templatename,model
    ranking_list = Book.objects.annotate(
        avg_rating=Avg("review__rate")).order_by("-avg_rating")

    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    # query = request.GET.get('number')
    # print(query)
    # print(ranking_list[0].avg_rating)
    return render(request, "book/index.html", {"object_list": object_list, "ranking_list": ranking_list, "page_obj": page_obj},)


# def logout_view(request):
#     logout(request)
#     return redirect("index")  # success_url
