from django.contrib import admin
from .models import Tickets,Comment;

@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
	list_display = ['user','name','subject','status','priority','updated'];


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['user','ticket','name','updated'];
