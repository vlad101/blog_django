from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/edit/<int:id>', views.post_edit, name='post-edit'),
    path('post/delete/<int:id>', views.post_delete, name='post-delete'),
    path('tag/<slug:slug>', views.TagDetailView.as_view(), name='tag-detail'),
    path('feed/', views.LatestPostFeed(), name='feed'),
    path("register/", views.register_request, name="register"),
    path('search/', views.search_results, name='search_results'),
    path('comment/delete/<int:id>', views.comment_delete, name='comment-delete'),
    path('comment/edit/<int:id>', views.comment_edit, name='comment-edit'),
    path('comment/<int:id>', views.comment_get_edit_form, name='comment-get-edit-form'),
]