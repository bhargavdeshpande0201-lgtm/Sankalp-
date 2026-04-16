from django.contrib import admin
from .models import Complaint, Comment


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'category', 'status', 'created_at']
    list_filter = ['category', 'status', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Details', {
            'fields': ('category', 'location', 'priority', 'status')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Options', {
            'fields': ('anonymous',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'complaint', 'created_at', 'is_staff']
    list_filter = ['created_at', 'is_staff']
    search_fields = ['text', 'user__username']
    readonly_fields = ['created_at']
