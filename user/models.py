from django.db import models
from django.conf import settings
from tickets.models import Category
# Create your models here.
# one to one relationship
#User >> Profile(pic,bir,ph,add)

class Profile(models.Model):#User
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE);
	photo = models.ImageField(null=True,blank=True,default='default.jpg');
	birthday = models.DateField(null=True,blank=True);
	phone = models.CharField(max_length=20,null=True,blank=True);
	address = models.TextField(null=True,blank=True);
	category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True);
	GENDER = (
				('other','Other'), # (Key,value)
				('male','Male'),
				('female','Female')
			);
	gender = models.CharField(max_length=100,choices = GENDER,default='other');
	def __str__(self):
		return self.user.username;
