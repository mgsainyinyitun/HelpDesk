from django.shortcuts import render,redirect
from . forms import UserRegistrationForm,ProfileForm,UserForm
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




