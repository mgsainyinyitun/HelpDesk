from django.db import models;
from django.contrib.auth.models import User;

class Tickets(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE);
	name = models.CharField(max_length = 200);
	subject = models.CharField(max_length = 300);
	description = models.TextField();
	attachment = models.FileField(upload_to = "tickets/files/",null=True,blank=True);
	STATUS_CHOICES = (
						('Open','open'), # (Key,value)
						('Pending','pending'),
						('Closed','closed')
					 );

	SET_PRIORITY = (
					('critical','Critical'),
					('urgent','Urgent'),
					('normal','Normal'),
					('not_important','Not Important'),
				   );

	status = models.CharField(max_length=100,choices=STATUS_CHOICES,default='open');
	priority = models.CharField(max_length=100,choices= SET_PRIORITY,default = 'not_important');
	created = models.DateTimeField(auto_now =True);
	updated = models.DateTimeField(auto_now_add = True);
	def __str__(self):
		return self.name;


class Comment(models.Model):
	ticket = models.ForeignKey(Tickets,on_delete=models.CASCADE);
	user = models.ForeignKey(User,on_delete=models.CASCADE);
	name = models.CharField(max_length=200);
	body = models.TextField();
	updated = models.DateTimeField(auto_now=True);
	def __str__(self):
		return self.name;