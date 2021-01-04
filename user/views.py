from django.shortcuts import render,redirect
from . forms import UserRegistrationForm,ProfileForm,UserForm,CustomerRegistrationForm,CustomerProfile,LoginForm      ;
from django.contrib.auth.decorators import login_required,user_passes_test;
from django.contrib import messages;
from django.contrib.auth.models import User;
from tickets.views import paginated;
from .auth import checkIfAdmin,checkIfTech,checkIfCustomer
from django.contrib.auth import authenticate


def login(request):
	if request.method == 'POST':
		form = LoginForm(data=request.POST);
		if form.is_valid():
			print(request.POST.get('password'));
			username = request.POST.get('username');
			password = request.POST.get('password');
			user = authenticate(username=username,password=password);

			print("user is ;;;",user);

	else:
		form = LoginForm();

	return render(request,'registration/login.html',{'form':form,

		});

@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(data=request.POST);
		user_profile = ProfileForm(data=request.POST, files=request.FILES);

		if user_form.is_valid() and user_profile.is_valid():
			new_user = user_form.save(commit=False);
			new_user.set_password(user_form.cleaned_data['password1']);
			new_user.is_staff = True;
			new_user.save();

			new_profile = user_profile.save(commit=False);
			new_profile.user = new_user;

			if new_profile.gender == 'female':
				new_profile.photo = 'default_female.jpg';
			new_profile.save();

			messages.success(request,"Technican created successfully");
			return redirect('dashboard');
	else:
		user_form = UserRegistrationForm();
		user_profile = ProfileForm();
	return render(request,'user/register.html',{'user_form':user_form,
												'user_profile':user_profile,
												'tech':'active',
		});



@login_required
def edit(request):
	if request.method == "POST":
		user_form = UserForm(instance= request.user,data=request.POST);
		profile_form = ProfileForm(instance=request.user.profile,data=request.POST,files=request.FILES);
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save();
			profile_form.save();
			messages.success(request,"Your Profile have been change successfully");
		else:
			messages.error(request,"Your Profile have not been change successfully. Try Again");
	else:
		user_form = UserForm(instance = request.user);
		profile_form = ProfileForm(instance= request.user.profile);
	return render(request,"user/edit.html",{"profile_form":profile_form,
											"user_form":user_form,
		})


@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def tech_view(request):
	users = User.objects.filter(is_staff = True);
	admin = 0;techs = 0;

	for user in users:
		if user.is_superuser:
			admin = admin+1;
		else:
			techs = techs+1;

	#pagination
	paginator,page_obj,users,page = paginated(request,users,3);

	return render(request,'user/tech_view.html',{'tech':'active',
												 'users':users,
												 'admin':admin,
												 'techs':techs,
												 'page_obj':page_obj,
												 'paginator':paginator,
												 'page':int(page)
													});

@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def role_view(request,role):
	if role == 'admin':
		users = User.objects.filter(is_superuser = True);
	else:
		users = User.objects.filter(is_staff = True,is_superuser=False);
	return render(request,'user/role_view.html',{'users':users,
												 'tech':'active',
												});


@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def user_detail_view(request,id):
	d_user = User.objects.get(pk=id);
	tech = '';
	customer = '';
	if d_user.is_superuser or d_user.is_staff:
		tech = 'active';
	else:
		customer='active';


	if request.method == "POST":
		user_form = UserForm(instance=d_user,data=request.POST);
		profile_form = ProfileForm(instance=d_user.profile,data=request.POST,files=request.FILES);
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save();
			profile_form.save();
			messages.success(request,"User data have been changed successfully");
		else:
			messages.error(request,"Cannot changed used data, try again!");
	else:
		user_form = UserForm(instance=d_user);
		profile_form = ProfileForm(instance=d_user.profile);

	return render(request,'user/user_detail_view.html',{'tech':tech,
														'customer':customer,
														'd_user':d_user,
														'user_form':user_form,
														'profile_form':profile_form,
														});

@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def customer_view(request):
	users = User.objects.filter(is_superuser=False,is_staff=False);
	return render(request,'user/customer_view.html',{ 'customer':'active',
													  'users':users
														});

@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def new_customer(request):
	if request.method == 'POST':
		customer_form = CustomerRegistrationForm(data=request.POST);
		profile_form = CustomerProfile(data=request.POST,files = request.FILES);
		if customer_form.is_valid() and profile_form.is_valid():
			new_customer = customer_form.save(commit = False);
			new_profile = profile_form.save(commit=False);
			new_customer.set_password(customer_form.cleaned_data['password1']);
			new_profile.user = new_customer;

			if new_profile.gender == 'female':
				new_profile.photo = 'default_female.jpg';

			new_customer.save();
			new_profile.save();
			messages.success(request,"Technican created successfully");
			return redirect('dashboard');
	else:
		customer_form = CustomerRegistrationForm();
		profile_form = CustomerProfile();

	return render(request,'user/new_customer.html',{ 'customer':'active',
													 'profile_form':profile_form,
													 'customer_form':customer_form,
														});


@user_passes_test(checkIfAdmin,login_url='error')
@login_required
def user_delete(request,id):
	user = User.objects.get(pk=id);

	role = user.is_staff; # true / false

	user.delete();
	messages.success(request,"User delete successful!");

	if role:
		return redirect('tech-view');
	else:
		return redirect('customer-view');

def error(request):
	return render(request,'user/error.html');
