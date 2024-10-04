# Define the Member class to represent a gym member and their check-in status.
class Member:
    def __init__(self, member_id, name, email):
        # Initialize the member with the provided attributes.
        self.member_id = member_id  # Unique identifier for the member.
        self.name = name  # Name of the member.
        self.email = email  # Email address of the member.
        self.checked_in = False  # Boolean attribute to track the check-in status of the member.

    # Method to mark the member as checked in.
    def check_in(self):
        self.checked_in = True  # Set the check-in status to True.

    # Method to mark the member as checked out.
    def check_out(self):
        self.checked_in = False  # Set the check-in status to False.
