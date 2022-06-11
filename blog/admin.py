from django.contrib import admin
from .models import Profile, Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user', 'created_on']


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {"slug": ("title", ), }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment_body', 'post', 'created_on',)
    list_filter = ('created_on',)
    search_fields = ('name', 'email', 'body')
