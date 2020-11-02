from django.shortcuts import render,redirect;
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

	pri_design = '';
	if ticket.priority == 'critical':
		pri_design = 'badge badge-danger';
	elif ticket.priority == 'urgent':
		pri_design = 'badge badge-warning';
	elif ticket.priority == 'normal':
		pri_design = 'badge badge-info';
	else:
		pri_design = 'badge badge-success';



	comments = Comment.objects.filter(ticket=ticket);
	#Comment Form handel
	if request.method == 'POST':
		#update data to database
		comment_form = CommentForm(data=request.POST);
		new_comment = comment_form.save(commit = False);
		new_comment.ticket = ticket;
		new_comment.user = request.user;
		new_comment.save();

	else:
		comment_form = CommentForm();

	return render(request,'tickets/ticket_detail.html',{'ticket':ticket,
														'comment_form':comment_form,
														'comments':comments,
														'pri_design':pri_design,
														});




@login_required
def change_status(request,id,status):
	ticket = Tickets.objects.get(pk = id);
	if status == 'open':
		ticket.status = 'Open';
	elif status == 'pending':
		ticket.status = 'Pending';
	else:
		ticket.status = 'Close';

	# pending # must be key (Pending)
	ticket.save();
	return redirect('ticket-detail',id=id);

	