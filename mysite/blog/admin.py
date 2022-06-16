from django.contrib import admin

from .models import Comment, Post

class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CommentInline]
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Post, PostAdmin)

admin.site.register(Comment)