from django.contrib import admin
from .models import Category, Job

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'salary', 'is_urgent', 'is_active', 'created_at')
    list_filter = ('is_urgent', 'is_active', 'gender', 'category')
    search_fields = ('title', 'location', 'description')