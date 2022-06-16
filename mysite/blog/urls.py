from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('tag/<slug:slug>', views.TagDetailView.as_view(), name='tag-detail'),
    path('feed/', views.LatestPostFeed(), name='feed'),
    path("register/", views.register_request, name="register"),
    path('comment/delete/<int:id>', views.delete_comment, name='comment-delete'),
]