from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import PostForm
from .models import Category, Post


def index(request):
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )[:5]

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        Q(pub_date__lte=timezone.now())
        & Q(is_published=True)
        & Q(category__is_published=True),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        category=category,
        pub_date__lte=timezone.now(),
        is_published=True
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)


class PostMixin:
    model = Post
    template_name = 'blog/create.html'

class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_absolute_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)
        
    def get_absolute_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'post_id': self.kwargs['pk']})


class PostDeleteView(LoginRequiredMixin, PostMixin, DeleteView):
    
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('blog:profile', kwargs={'username': self.request.user.username})