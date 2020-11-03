from django.shortcuts import render,redirect;
from django.contrib.auth.decorators import login_required;
from .models import Tickets,Comment;
from .forms import CommentForm, TicketForm;
from django.contrib.auth.models import User;
from django import forms;

@login_required
def dashboard(request):
	open=0;
	closed =0;
	pending = 0;
	if request.user.is_superuser or request.user.is_staff:
		tickets = Tickets.objects.all();
	else:
		tickets = Tickets.objects.filter(user=request.user);

	for ticket in tickets:
		if ticket.status == 'Open':
			open = open + 1;
		elif ticket.status == 'Closed':
			closed = closed + 1;
		elif ticket.status == 'Pending':
			pending = pending +1;


	#print('User',user);
	return render(request,'user/dashboard.html',{'tickets':tickets,
												 'open':open,
												 'closed':closed,
												 'pending':pending,
												});


@login_required
def ticket_detail(request,id):
	ticket = Tickets.objects.get(pk=id);

	pri_design = '';
	priority = '';
	if ticket.priority == 'critical':
		pri_design = 'btn btn-danger rounded-pill';
		priority = "Critical";
	elif ticket.priority == 'urgent':
		pri_design = 'btn btn-warning rounded-pill';
		priority = 'Urgent';
	elif ticket.priority == 'normal':
		pri_design = 'btn btn-info rounded-pill';
		priority = "Normal";
	else:
		pri_design = 'btn btn-success rounded-pill';
		priority = "Not Important";



	comments = Comment.objects.filter(ticket=ticket);
	#Comment Form handel
	if request.method == 'POST':
		#update data to database
		comment_form = CommentForm(data=request.POST);
		if comment_form.is_valid():
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
														'priority':priority,
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


@login_required
def create_ticket(request):
	if request.method == 'POST':
		new_form = TicketForm(data= request.POST,files = request.FILES);
		if new_form.is_valid():
			new_ticket = new_form.save(commit = False);
			new_ticket.user = request.user;
			new_ticket.name = request.user.username;
			new_ticket.save();
			return redirect('dashboard');
	else:
		new_form = TicketForm();
	return render(request,'tickets/create_ticket.html' ,{'new_form':new_form});