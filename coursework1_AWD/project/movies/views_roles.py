# Function to check if a user is an admin
def is_admin(user):
    # Returns True if the user is authenticated and has the 'admin' role
    return user.is_authenticated and user.role == 'admin'

# Function to check if a user is a customer
def is_customer(user):
    # Returns True if the user is authenticated and has the 'customer' role
    return user.is_authenticated and user.role == 'customer'
