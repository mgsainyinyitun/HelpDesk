from django import forms;
from .models import Comment, Tickets,Category;
from crispy_forms.helper import FormHelper

class CommentForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs);
		self.helper = FormHelper(self);
		self.helper.form_show_labels = False;

	class Meta:
		model = Comment;
		fields = ('comment',);

class TicketForm(forms.ModelForm):
	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs);
		self.helper = FormHelper(self);
		self.helper.form_show_labels = False;
	class Meta:
		model =  Tickets;
		fields = ('name','subject','description','priority','attachment');

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category;
		fields = ('name',);