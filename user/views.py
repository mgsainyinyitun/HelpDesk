from django.shortcuts import render,redirect
from . forms import UserRegistrationForm,ProfileForm,UserForm
from django.contrib.auth.decorators import login_required;
from django.contrib import messages;



@login_required
def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(data=request.POST);
		user_profile = ProfileForm(data=request.POST, files=request.FILES);

		if user_form.is_valid() and user_profile.is_valid():
			new_user = user_form.save(commit=False);
			new_user.set_password(user_form.cleaned_data['password1']);
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




