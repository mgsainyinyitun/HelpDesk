from django.contrib import admin
from .models import Tickets,Comment,Category;

@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
	list_display = ['user','name','subject','status','priority','updated','created'];

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['user','ticket','updated'];

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name','slug'];
	prepopulated_fields = {"slug": ("name",)}
