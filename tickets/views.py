from django.shortcuts import render
from django.contrib.auth.decorators import login_required;
from .models import Tickets,Comment;
from .forms import CommentForm;
from django.contrib.auth.models import User;
from django import forms;

@login_required
def dashboard(request):
	tickets = Tickets.objects.all();
	#print('User',user);
	return render(request,'user/dashboard.html',{'tickets':tickets});


@login_required
def ticket_detail(request,id):
	ticket = Tickets.objects.get(pk=id);
	comments = Comment.objects.filter(ticket=ticket);
	#Comment Form handel
	if request.method == 'POST':
		#update data to database
		comment_form = CommentForm(data=request.POST);
		new_comment = comment_form.save(commit = False);
		new_comment.ticket = ticket;
		new_comment.user = user;
		new_comment.save();

	else:
		comment_form = CommentForm();

	return render(request,'tickets/ticket_detail.html',{'ticket':ticket,
														'comment_form':comment_form,
														'comments':comments,
														});