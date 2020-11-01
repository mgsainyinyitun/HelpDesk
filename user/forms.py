from django import forms
from django.contrib.auth.models import User;
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password',widget=forms.PasswordInput);
	password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput);
	class Meta:
		model = User;
		fields = ('username','first_name','last_name','email');

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password2'] != cd['password1']:
			raise forms.ValidationError("Your password does not equal");
		return cd['password2'];


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('photo','birthday','phone','address');


class UserForm(forms.ModelForm):
	class Meta:
		model = User;
		fields = ('first_name','last_name','email');



