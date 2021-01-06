from django.shortcuts import render,redirect;
from django.contrib.auth.decorators import login_required,user_passes_test;
from .models import Tickets,Comment,Category;
from .forms import CommentForm, TicketForm,CategoryForm;
from django.contrib.auth.models import User;
from django import forms;
from django.core.paginator import Paginator,PageNotAnInteger;
from django.contrib import messages;
from django.utils.text import slugify;
from user.auth import checkIfAdmin,checkIfTech,checkIfCustomer,checkIfAdminOrTech
from .Calculation import num_of_priority,num_of_category,num_of_general;
from .utils import render_to_pdf;
from django.http import HttpResponse;
import datetime;


@login_required
def render_pdf(request):
	tickets,cat_none = tickets_filter(request);
	data = [];
	for ticket in tickets:
		obj = {	"user":ticket.user.username,
				"subject":ticket.subject,
				"department":ticket.name,
				"status":ticket.status,
				"priority":ticket.priority,
				"category":ticket.category,
				"date":ticket.created,
		}
		data.append(obj);

	tickets = {"tickets":data};

	pdf = render_to_pdf('tickets/tickets_pdf.html',tickets);
	return HttpResponse(pdf,content_type="application/pdf")


@login_required
def dashboard(request):
	open=0;closed =0;pending = 0;
	categories = Category.objects.all();

	if request.user.is_superuser or request.user.is_staff:
		if request.user.is_staff and not request.user.is_superuser:
			if request.user.profile.category:
				tickets = Tickets.objects.filter(category = request.user.profile.category).order_by('-created');
			else:
				tickets =  Tickets.objects.all().order_by('-created');
		else:
			tickets = Tickets.objects.all().order_by('-created');
	else:
		tickets = Tickets.objects.filter(user=request.user).order_by('-created');
	
	for ticket in tickets:
		if ticket.status == 'Open':
			open = open + 1;
		elif ticket.status == 'Closed':
			closed = closed + 1;
		elif ticket.status == 'Pending':
			pending = pending +1;


	critical,urgent,normal,not_important = num_of_priority();

	cat_number = num_of_category();

	#paginator function
	paginator,page_obj,tickets,page = paginated(request,tickets,3);

	total_tickets,admin,technician,customer  = num_of_general();	
	print('tickets::',tickets)


	return render(request,'user/dashboard.html',{'tickets':tickets,
												 'open':open,
												 'closed':closed,
												 'pending':pending,
												 'page_obj':page_obj,
												 'dashboard':'active',
												 'critical':critical,
												 'urgent':urgent,
												 'normal':normal,
												 'not_important':not_important,
												 'categories':categories,
												 'cat_number':cat_number,
												 'total_tickets':total_tickets,
												 'admin':admin,
												 'technician':technician,
												 'customer':customer,
												 'tot_tech':admin+technician,
												 'paginator':paginator,
												 'page':int(page),
												});


@login_required
def ticket_detail(request,id):
	ticket = Tickets.objects.get(pk=id);
	categories = Category.objects.all();

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
		ticket_form = TicketForm(instance = ticket,data=request.POST,files=request.FILES);

		print("Comment:::",comment_form);

		
		if comment_form.is_valid():
			new_comment = comment_form.save(commit = False);
			new_comment.ticket = ticket;
			new_comment.user = request.user;
			new_comment.save();
			comment_form = CommentForm();

		if ticket_form.is_valid():
			new_ticket = ticket_form.save();

	else:
		comment_form = CommentForm();
		ticket_form = TicketForm(instance=ticket);

	return render(request,'tickets/ticket_detail.html',{'ticket':ticket,
														'comment_form':comment_form,
														'comments':comments,
														'pri_design':pri_design,
														'priority':priority,
														'nav_ticket':'active',
														'categories':categories,
														'ticket_form':ticket_form
														});



@user_passes_test(checkIfAdminOrTech,login_url='error')
@login_required
def change_status(request,id,status):
	ticket = Tickets.objects.get(pk = id);
	if status == 'open':
		ticket.status = 'Open';
	elif status == 'pending':
		ticket.status = 'Pending';
	else:
		ticket.status = 'Closed';

	# pending # must be key (Pending)
	ticket.save();
	messages.success(request,"Status have been change successfully");
	return redirect('ticket-detail',id=id);

@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def change_category(request,id,category):
	ticket = Tickets.objects.get(pk = id);
	cat = Category.objects.get(slug = category);
	ticket.category = cat;
	ticket.save();
	messages.success(request,"Category have been Assigned successfully");
	return redirect('ticket-detail',id = id);


@user_passes_test(checkIfCustomer,login_url='error')
@login_required
def create_ticket(request):
	if request.method == 'POST':
		new_form = TicketForm(data= request.POST,files = request.FILES);
		if new_form.is_valid():
			new_ticket = new_form.save(commit = False);
			new_ticket.user = request.user;
			#new_ticket.name = request.user.username;
			new_ticket.save();
			messages.success('successfully created ticket');
			return redirect('dashboard');
	else:
		new_form = TicketForm();
	return render(request,'tickets/create_ticket.html' ,{'new_form':new_form,
														 'new_ticket':'active',
															});


@login_required
def status_view(request,status):
	if status == 'recent':
		return redirect('dashboard');

	tickets = Tickets.objects.filter(status = status.capitalize()).order_by('-created');

	if not request.user.is_superuser and not request.user.is_staff:
		tickets = tickets.filter(user= request.user).order_by('-created');

	number = 0;
	# Key <Open, Closed , Pending>
	for _ in tickets:
		number = number+1; #tickets.count

	paginator,page_obj,tickets,page = paginated(request,tickets,3);

	return render(request,'tickets/status_view.html',{'tickets':tickets,
													  'status':status,
													  'number':number,
													  'page_obj':page_obj,
													  'dashboard':'active',
													  'paginator':paginator,
													  'page':int(page),
														});
#category
@user_passes_test(checkIfAdminOrTech,login_url='error')
@login_required
def new_category(request):
	if request.method == 'POST' and request.user.is_superuser:
		category_form = CategoryForm(data=request.POST);
		if category_form.is_valid():
			new_category = category_form.save(commit=False);
			new_category.slug = slugify(new_category.name);
			new_category.save();
			messages.success(request,"Category added successfully");
			category_form = CategoryForm();
		else:
			messages.error(request,"Cannot add category, try again!");
	else:
		category_form= CategoryForm();

	categories = Category.objects.all();

	return render(request,'tickets/new_category.html',{ 'category':'active',
														'category_form':category_form,
														'categories':categories,
														});

@user_passes_test(checkIfAdmin,login_url='error')
def delete_category(request,cat):
	category = Category.objects.get(slug=cat);
	category.delete();
	messages.success(request,"successfully delete category!")
	return redirect('new-category');


@user_passes_test(checkIfAdmin,login_url='error')
def edit_category(request,cat):
	category = Category.objects.get(slug=cat);
	name = request.GET.get('name');
	category.name = name;
	category.slug = slugify(name);
	category.save();
	messages.success(request,"Successfully edit Category");
	return redirect('new-category');



find = {
	'status':'all',
	'priority':'all',
	'category':'all',
	'cat_none':False,
	'sort':'none',
	'order':'descending',
}

date = {
	'start-date':None,
	'end-date':None,
}


def tickets_filter(request):
	status = request.GET.get('status'); #all
	priority = request.GET.get('priority'); # none
	category = request.GET.get('category'); # all,.......
	sort = request.GET.get('sort');
	order = request.GET.get('order');

	start_date = request.GET.get('start-date'); # date, null
	end_date = request.GET.get('end-date');
	# date >> dirct
	# null >> 
	if start_date and end_date:
		date['start-date'] = start_date;
		date['end-date'] = end_date;
	elif start_date:
		date['start-date'] = start_date;
		date['end-date'] = datetime.date.today();

	# SORTING # sort not by user id
	if sort:
		find['sort'] = sort;
	if order:
		find['order'] = order;
	if find['order'] == 'ascending':
		if find['sort'] == 'date':
			tickets =Tickets.objects.all().order_by('created');
		elif find['sort'] == 'user':
			tickets = Tickets.objects.all().order_by('user__username');
		elif find['sort'] == 'department':
			tickets = Tickets.objects.all().order_by('name');
		else:
			tickets = Tickets.objects.all();
	elif find['order'] == 'descending':
		if find['sort'] == 'date':
			tickets =Tickets.objects.all().order_by('-created');
		elif find['sort'] == 'user':
			tickets = Tickets.objects.all().order_by('-user__username');
		elif find['sort'] == 'department':
			tickets = Tickets.objects.all().order_by('-name');

		else:
			tickets = Tickets.objects.all();

	#SEARCHING
	search_txt = request.GET.get('search');
	#print("SEARCH_TXT",search_txt)
	if search_txt:
		tickets = tickets & Tickets.objects.filter(subject__icontains = search_txt);

	# STATUS FILTER
	if (status and status != 'all') or (find['status'] != 'all' and status != 'all'):
		if status:
			find['status'] = status;
		tickets = tickets & Tickets.objects.filter(status=find['status'].capitalize());#status=all
	else:
		find['status'] = 'all';


	# PRIORITY FILTER
	if (priority and priority != 'all') or (find['priority'] != 'all' and priority != 'all'):
		if priority:
			find['priority'] = priority;
		tickets = tickets & Tickets.objects.filter(priority=find['priority']);
	else:
		find['priority'] = 'all';

	# CATEGORY FILTER
	if (category and category != 'all' and category != 'none') or (find['category'] != 'all' and category != 'all' and category != 'none'):
		if category:
			find['category'] = category;

		cat = Category.objects.get(slug = find['category']); #####Not None
		tickets = tickets & Tickets.objects.filter(category = cat);
	else:
		find['category'] = 'all';


	# FILTER FOR CATEGORY NONE

	# category != Null && category != none
	# must reset mem when category == all, other cat.....
	if (category and category != 'none'):
		find['cat_none'] = False;


	# exclude all category # exclude(category = 'computer-error');
	cat_none  = False;
	if (category == 'none' or find['cat_none'] == True):
		if category == 'none':
			find['cat_none'] = True; # Must be false if 

		categories = Category.objects.all();
		for cat in categories:
			tickets = tickets & Tickets.objects.exclude(category = cat);
		cat_none = True;


	if date['start-date'] and date['end-date']:
		tickets = tickets & Tickets.objects.filter(created__range = [date['start-date'],date['end-date']])


	return tickets,cat_none;


#tickets
@login_required
def tickets(request):
	categories = Category.objects.all();
	tickets,cat_none = tickets_filter(request);
	clear = False;

	if date['start-date'] and date['end-date']:
		clear = True;
	else:
		clear = False;



	paginator,page_obj,tickets,page = paginated(request,tickets,5);

	return render(request,'tickets/tickets.html',{'nav_ticket':'active',
												  'categories':categories,
												  'tickets':tickets,
												  'find':find,
												  'cat_none':cat_none,
												  'page_obj':page_obj,
												  'paginator':paginator,
												  'page':int(page),
												  'clear':clear,
													});


def clear_date(request):
	date['start-date'] = None;
	date['end-date'] = None;
	return redirect('tickets');

def paginated(request,objects,number):
	paginator = Paginator(objects,number);
	try:
		page = request.GET.get('page'); # page no variable 
		page_obj =paginator.get_page(page);
		objects = paginator.page(page);
	except PageNotAnInteger:
		page = 1;
		page_obj = paginator.get_page(1);
		objects = paginator.page(1);

	return paginator,page_obj,objects,page;
