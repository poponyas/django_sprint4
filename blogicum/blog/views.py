from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Category, Post


class HomeBlog(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.select_related(
            'category', 'location', 'author'
        ).filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class CategoryListView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10 

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return (
            Post.objects.select_related('category', 'location', 'author')
            .filter(
                category=self.category,
                pub_date__lte=timezone.now(),
                is_published=True
            )
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


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