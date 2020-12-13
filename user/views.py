from django.shortcuts import render,redirect
from . forms import UserRegistrationForm,ProfileForm,UserForm,CustomerRegistrationForm;
from django.contrib.auth.decorators import login_required;
from django.contrib import messages;
from django.contrib.auth.models import User;
from tickets.views import paginated;

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

			return redirect('login');
	else:
		user_form = UserRegistrationForm();
		user_profile = ProfileForm();
	return render(request,'user/register.html',{'user_form':user_form,
												'user_profile':user_profile,
												'tech':'active',
		});



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
	page_obj,users = paginated(request,users,5);

	return render(request,'user/tech_view.html',{'tech':'active',
												 'users':users,
												 'admin':admin,
												 'techs':techs,
												 'page_obj':page_obj,
													});


@login_required
def role_view(request,role):
	if role == 'admin':
		users = User.objects.filter(is_superuser = True);
	else:
		users = User.objects.filter(is_staff = True,is_superuser=False);
	return render(request,'user/role_view.html',{'users':users,
												 'tech':'active',
												});



@login_required
def user_detail_view(request,id):
	d_user = User.objects.get(pk=id);
	tech = '';
	customer = '';
	if d_user.is_superuser or d_user.is_staff:
		tech = 'active';
	else:
		customer='active';

	if request.method== "POST":
		user_form = UserForm(instance=d_user,data = request.POST);
		profile_form = ProfileForm(instance=d_user.profile,data=request.POST,files = request.FILES);
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save();
			profile_form.save();
			messages.success(request,"Edit successfully");
		else:
			messages.error(request,"Edit Unsuccessfully");
	else:
		user_form = UserForm(instance=d_user);
		profile_form = ProfileForm(instance=d_user.profile);

	return render(request,'user/user_detail_view.html',{'tech':tech,
														'customer':customer,
														'd_user':d_user,
														'user_form':user_form,
														'profile_form':profile_form,
														});

# for customer

@login_required

def customer_view(request):
	users = User.objects.filter(is_superuser=False,is_staff=False);
	return render(request,'user/customer_view.html',{ 'customer':'active',
													  'users':users
														});


@login_required
def new_customer(request):
	if request.method == 'POST':
		customer_form = CustomerRegistrationForm(data=request.POST);
		profile_form = ProfileForm(data=request.POST,files = request.FILES);
		if customer_form.is_valid() and profile_form.is_valid():
			new_customer = customer_form.save(commit = False);
			new_profile = profile_form.save(commit=False);
			new_customer.set_password(customer_form.cleaned_data['password1']);
			new_profile.user = new_customer;

			if new_profile.gender == 'female':
				new_profile.photo = 'default_female.jpg';

			new_customer.save();
			new_profile.save();
			return redirect('dashboard');
	else:
		customer_form = CustomerRegistrationForm();
		profile_form = ProfileForm();

	return render(request,'user/new_customer.html',{ 'customer':'active',
													 'profile_form':profile_form,
													 'customer_form':customer_form,
														});



@login_required
def user_delete(request,id):
	user = User.objects.get(pk=id);

	role = user.is_staff; # true / false

	user.delete();

	if role:
		return redirect('tech-view');
	else:
		return redirect('customer-view');



