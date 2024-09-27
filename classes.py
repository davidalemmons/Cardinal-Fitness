class ClassSchedule:
    def __init__(self, class_id, class_name, instructor, time, capacity):
        self.class_id = class_id
        self.class_name = class_name
        self.instructor = instructor
        self.time = time
        self.capacity = capacity
        self.enrolled_members = []

    def enroll_member(self, member):
        if len(self.enrolled_members) < self.capacity:
            self.enrolled_members.append(member)
            print(f"{member.name} enrolled in {self.class_name}.")
        else:
            print(f"Class {self.class_name} is full.")

    def display_class_info(self):
        enrolled = [member.name for member in self.enrolled_members]
        return f"Class: {self.class_name}, Instructor: {self.instructor}, Time: {self.time}, Enrolled: {enrolled}"
