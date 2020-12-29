from .models import Tickets,Comment,Category;
from django.contrib.auth.models import User;

def num_of_priority():
	tickets = Tickets.objects.all();

	critical = 0;
	urgent = 0;
	normal = 0;
	not_important = 0;

	for ticket in tickets:
		if ticket.priority == 'critical':
			critical = critical + 1;
		elif ticket.priority == 'urgent':
			urgent = urgent + 1;
		elif ticket.priority == 'normal':
			normal = normal + 1;
		elif ticket.priority == 'not_important':
			not_important = not_important + 1;

	return critical,urgent,normal,not_important;


def num_of_general():
	tickets = Tickets.objects.all();
	users = User.objects.all();
	total_tickets = tickets.count();
	
	if total_tickets == 0:
		total_tickets = 1;


	admin = 0; customer = 0;technician = 0;

	for user in users:
		if user.is_superuser:
			admin  = admin +1;
		elif user.is_staff and not user.is_superuser:
			technician = technician + 1;
		elif not user.is_superuser and not user.is_staff:
			customer = customer + 1;

	return total_tickets,admin,technician,customer;



def num_of_category():
	tickets = Tickets.objects.all();
	categories = Category.objects.all();

	total_ticket = tickets.count();
	has_category = 0;
	data = {};

	#{ name : { number: 10,
	#			percentage: 10%,
	#			color : red,
	#}
	#
	color = ["blue","darkviolet","darkgreen","purple","Crimson","MediumVioletRed","orange","indigo","lime","maroon"];
	color_index  = 0;
	for category in categories:
		temp = Tickets.objects.filter(category = category);
		number = temp.count();
		has_category = has_category + number;	
		data[category.name] = { "number":number,
								"percentage":  round((number/total_ticket)*100,1),
								"color":color[color_index]
								}
		color_index = color_index + 1;
		if color_index >= 10:
			color_index = 0;
		
	data["None"] = { "number":total_ticket-has_category,
					 "percentage": round(((total_ticket-has_category)/total_ticket)*100,1),
					 "color":"gray"
					}


	#{ "computer-err":10,
	#  "network-err":5,
	#}
	return data;


