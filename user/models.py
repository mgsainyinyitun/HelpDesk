from django.db import models
from django.conf import settings
# Create your models here.
# one to one relationship
#User >> Profile(pic,bir,ph,add)

class Profile(models.Model):#User
	user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE);
	photo = models.ImageField(null=True,blank=True);
	birthday = models.DateField(null=True,blank=True);
	phone = models.CharField(max_length=20,null=True,blank=True);
	address = models.TextField(null=True,blank=True);
	def __str__(self):
		return self.user.username;
