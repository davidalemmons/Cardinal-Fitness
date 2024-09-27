# Member class (for reference)
class Member:
    def __init__(self, member_id, name, email):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.checked_in = False  # Attribute to track if the member is checked in

    def check_in(self):
        self.checked_in = True

    def check_out(self):
        self.checked_in = False
