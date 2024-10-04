# Define the ClassSchedule class to manage the scheduling and enrollment of fitness classes.
class ClassSchedule:
    def __init__(self, class_id, class_name, instructor, time, capacity):
        # Initialize the class with the provided attributes.
        self.class_id = class_id  # Unique identifier for the class.
        self.class_name = class_name  # Name of the fitness class.
        self.instructor = instructor  # Instructor's name for the class.
        self.time = time  # Scheduled time for the class.
        self.capacity = capacity  # Maximum number of members allowed in the class.
        self.enrolled_members = []  # List to keep track of members enrolled in the class.

    # Method to enroll a member into the class.
    def enroll_member(self, member):
        # Check if the class has not reached its capacity.
        if len(self.enrolled_members) < self.capacity:
            # Add the member to the enrolled members list.
            self.enrolled_members.append(member)
            print(f"{member.name} enrolled in {self.class_name}.")  # Print a success message.
        else:
            # Print a message indicating the class is full.
            print(f"Class {self.class_name} is full.")

    # Method to display information about the class, including enrolled members.
    def display_class_info(self):
        # Create a list of names for the enrolled members.
        enrolled = [member.name for member in self.enrolled_members]
        # Return a formatted string with class details.
        return f"Class: {self.class_name}, Instructor: {self.instructor}, Time: {self.time}, Enrolled: {enrolled}"
