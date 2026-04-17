from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeBlog.as_view(), name='index'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.CategoryListView.as_view(),
         name='category_posts'
         ),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
]
