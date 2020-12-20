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
from django.http import HttpResponse
from .utils import render_to_pdf;

def generatePDF(request):
	
	#tickets = Tickets.objects.all();
	data = {
             'today': "10.20.2020", 
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        };

	pdf = render_to_pdf('tickets/invoice.html',data)
	return HttpResponse(pdf,content_type='application/pdf')


@login_required
def dashboard(request):
	open=0;closed =0;pending = 0;
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

	print('open:::',open);
	print('closed:::',closed);
	print('pending:::',pending);

	#paginator function
	page_obj,tickets = paginated(request,tickets,3);	

	#print('User',user);
	return render(request,'user/dashboard.html',{'tickets':tickets,
												 'open':open,
												 'closed':closed,
												 'pending':pending,
												 'page_obj':page_obj,
												 'dashboard':'active',
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
		if comment_form.is_valid():
			new_comment = comment_form.save(commit = False);
			new_comment.ticket = ticket;
			new_comment.user = request.user;
			new_comment.save();
			comment_form = CommentForm();

	else:
		comment_form = CommentForm();

	return render(request,'tickets/ticket_detail.html',{'ticket':ticket,
														'comment_form':comment_form,
														'comments':comments,
														'pri_design':pri_design,
														'priority':priority,
														'nav_ticket':'active',
														'categories':categories
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
			return redirect('dashboard');
	else:
		new_form = TicketForm();
	return render(request,'tickets/create_ticket.html' ,{'new_form':new_form,
														 'dashboard':'active',
															});


@login_required
def status_view(request,status):
	if status == 'recent':
		return redirect('dashboard');

	tickets = Tickets.objects.filter(status = status.capitalize());

	if not request.user.is_superuser and not request.user.is_staff:
		tickets = tickets.filter(user= request.user);

	number = 0;
	# Key <Open, Closed , Pending>
	for _ in tickets:
		number = number+1; #tickets.count

	page_obj,tickets = paginated(request,tickets,3);

	return render(request,'tickets/status_view.html',{'tickets':tickets,
													  'status':status,
													  'number':number,
													  'page_obj':page_obj,
													  'dashboard':'active',
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

#tickets
def tickets(request):
	categories = Category.objects.all();
	status = request.GET.get('status'); #all
	priority = request.GET.get('priority'); # none
	category = request.GET.get('category'); # all,.......
	sort = request.GET.get('sort');
	order = request.GET.get('order');
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


	for k,f in find.items():
		print(f);

	page_obj,tickets = paginated(request,tickets,5);
	return render(request,'tickets/tickets.html',{'nav_ticket':'active',
												  'categories':categories,
												  'tickets':tickets,
												  'find':find,
												  'cat_none':cat_none,
												  'page_obj':page_obj
													});

def paginated(request,objects,number):
	paginator = Paginator(objects,number);
	try:
		page = request.GET.get('page'); # page no variable 
		page_obj =paginator.get_page(page);
		objects = paginator.page(page);
	except PageNotAnInteger:
		page_obj = paginator.get_page(1);
		objects = paginator.page(1);

	return page_obj,objects;
