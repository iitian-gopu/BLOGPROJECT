from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=['title','status','author','slug','body','publish','created','updated','image']
    prepopulated_fields={'slug':('title',)}
    list_filter=('status','author','publish','created','updated','title',)
    search_fields=('title', 'body')
    raw_id_fields=('author',)
    date_hierarchy=('publish')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on','updated_on','active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)