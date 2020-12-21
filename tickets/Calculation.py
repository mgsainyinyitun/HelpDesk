from .models import Tickets,Comment,Category;

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


def num_of_category():
	tickets = Tickets.objects.all();
	categories = Category.objects.all();

	total_ticket = tickets.count();
	has_category = 0;
	data = {};

	for category in categories:
		temp = Tickets.objects.filter(category = category);
		number = temp.count();
		has_category = has_category + number;	
		data[category.slug] = number;
		

	data["None"] = total_ticket - has_category;

	return data;


