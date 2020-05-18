from django.contrib import admin

from .models import Post, Comment, Vote  # add this line


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


class VoteInLine(admin.TabularInline):
    model = Vote
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fieldsets = [(None, {
        "fields": ["title", 'text', 'user', 'votes']
    }), ('Date Information', {
        'fields': [],
        'classes': ['collapse']
    })]
    inlines = [CommentInLine, VoteInLine]


admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
