def checkIfAdmin(user):
	return user.is_superuser;

def checkIfTech(user):
	return not user.is_superuser and user.is_staff;

def checkIfAdminOrTech(user):
	return user.is_superuser or user.is_staff;

def checkIfCustomer(user):
	return not user.is_superuser and not user.is_staff;

