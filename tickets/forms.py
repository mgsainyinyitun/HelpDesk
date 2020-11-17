from django import forms;
from .models import Comment, Tickets,Category;

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment;
		fields = ('name','body');

class TicketForm(forms.ModelForm):
	class Meta:
		model =  Tickets;
		fields = ('name','subject','description','priority','attachment');

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category;
		fields = ('name',);