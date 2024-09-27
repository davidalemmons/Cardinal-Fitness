import json
import re
import tkinter as tk
from tkinter import messagebox
from members import Member
from classes import ClassSchedule
from notifications import Notification

# Load configuration from config.json
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# Main App Class
class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cardinal Fitness Check-In System")
        self.configure(bg='#ffffff')  # White background

        # Set to full-screen on startup
        self.attributes('-fullscreen', True)

        # Bind Esc key to exit full-screen mode
        self.bind("<Escape>", self.exit_fullscreen)

        # Load configuration
        self.config = load_config()
        self.default_capacity = self.config['default_class_capacity']
        self.default_notification_message = self.config['notification_message']

        # Initialize members and classes
        self.members = []
        self.classes = {
            "Yoga": ClassSchedule("C001", "Yoga", "Alice Johnson", "10:00 AM", self.default_capacity),
            "Spinning": ClassSchedule("C002", "Spinning", "John Doe", "12:00 PM", self.default_capacity)
        }

        # Initialize all frames (for navigation)
        self.frames = {}
        self.create_frames()

        # Show the main menu initially
        self.show_frame("MainMenu")

    def create_frames(self):
        # Create all the frames
        for F in (MainMenu, CheckInFrame, EnrollFrame, ViewClassesFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Make the frames take up all available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def exit_fullscreen(self, event=None):
        '''Exit full-screen mode when Esc is pressed'''
        self.attributes('-fullscreen', False)

# Main Menu Frame
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#ffffff')

        # Centering contents using pack
        title_label = tk.Label(self, text="Cardinal Fitness", font=("Arial", 64, "bold"), bg="#ffffff", fg="#ff0000")
        title_label.pack(pady=20, anchor='center')

        check_in_button = tk.Button(self, text="Check In/Checkout", command=lambda: controller.show_frame("CheckInFrame"), bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        check_in_button.place( anchor='center', relx=0.5, rely=0.35)

        enroll_button = tk.Button(self, text="Enroll Member", command=lambda: controller.show_frame("EnrollFrame"), bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        enroll_button.place( anchor='center', relx=0.5, rely= 0.5)

        view_classes_button = tk.Button(self, text="View Classes", command=lambda: controller.show_frame("ViewClassesFrame"), bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        view_classes_button.place(anchor='center', relx=0.5, rely= 0.65)

# Check-In Frame
class CheckInFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#ffffff')

        label = tk.Label(self, text="Member Check-In/Check-Out", font=("Arial", 64, "bold"), bg="#ffffff", fg="#ff0000")
        label.pack(pady=10, anchor='center')

        self.member_id_entry = tk.Entry(self, width=45)
        self.member_id_entry.place(anchor='center', relx=0.5, rely=0.25)

        # Check In Button
        check_in_button = tk.Button(self, text="Check In", command=self.check_in_member, bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        check_in_button.place(anchor='center', relx=0.5, rely=0.35)

        # Check Out Button
        check_out_button = tk.Button(self, text="Check Out", command=self.check_out_member, bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        check_out_button.place(anchor='center', relx=0.5, rely=0.5)

        # Back to Main Menu Button
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), bg="#cccccc", font=("Arial", 24))
        back_button.place(anchor='center', relx=0.5, rely=0.65)

    def check_in_member(self):
        member_id = self.member_id_entry.get()
        member = next((m for m in self.controller.members if m.member_id == member_id), None)

        if member:
            if member.checked_in:
                # Notify the member if they are already checked in
                messagebox.showinfo("Already Checked In", f"{member.name}, you are already checked in.")
            else:
                member.check_in()
                messagebox.showinfo("Check In", f"{member.name} has successfully checked in.")
        else:
            messagebox.showwarning("Check In", "Member not found. Please enroll first.")

    def check_out_member(self):
        member_id = self.member_id_entry.get()
        member = next((m for m in self.controller.members if m.member_id == member_id), None)

        if member:
            if not member.checked_in:
                # Notify the member if they are already checked out
                messagebox.showinfo("Already Checked Out", f"{member.name}, you are already checked out.")
            else:
                member.check_out()
                messagebox.showinfo("Check Out", f"{member.name} has successfully checked out.")
        else:
            messagebox.showwarning("Check Out", "Member not found. Please enroll first.")

# Enroll Member Frame
class EnrollFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#ffffff')

        label = tk.Label(self, text="Enroll Member", font=("Arial", 64, "bold"), bg="#ffffff", fg="#ff0000")
        label.pack(pady=10, anchor='center')

        tk.Label(self, text="Member Name:", font=("Arial", 24), bg="#ffffff").place(anchor='center', relx=0.5, rely=0.2)
        self.member_name_entry = tk.Entry(self, width=30)
        self.member_name_entry.place(anchor='center', relx=0.5, rely=0.25)

        tk.Label(self, text="Email:", font=("Arial", 24), bg="#ffffff").place(anchor='center', relx=0.5, rely=0.3)
        self.member_email_entry = tk.Entry(self, width=30)
        self.member_email_entry.place(anchor='center', relx=0.5, rely=0.35)

        enroll_button = tk.Button(self, text="Enroll", command=self.enroll_member, bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        enroll_button.place(anchor='center', relx=0.5, rely=0.5)

        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), bg="#cccccc", font=("Arial", 24))
        back_button.place(anchor='center', relx=0.5, rely=0.65)

    def enroll_member(self):
        member_name = self.member_name_entry.get()
        member_email = self.member_email_entry.get()
    
        # Email validation function
        def is_valid_email(email):
            # Regular expression for basic email validation
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            return re.match(email_regex, email) is not None

        # Check if email input is valid
        if not is_valid_email(member_email):
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            return

        # Check if email is already in use
        for member in self.controller.members:
            if member.email == member_email:
                messagebox.showwarning("Duplicate Email", "This email is already in use. Please use a different email.")
                return

        # Proceed with member enrollment if email is valid and not a duplicate
        if member_name and member_email:
            new_member_id = f"M{len(self.controller.members) + 1:03d}"  # Generate new member ID
            new_member = Member(new_member_id, member_name, member_email)
            self.controller.members.append(new_member)

            # Send a notification upon successful enrollment in gym membership
            notification = Notification(self.controller.default_notification_message, new_member)
            notification.send_notification()

            # Display a message to indicate success
            messagebox.showinfo("Enrollment", f"{new_member.name} has been enrolled in the gym with ID: {new_member_id}. Notification sent.")
        else:
            messagebox.showwarning("Enrollment", "Please fill out both fields.")

# View Classes Frame with Sign Up and Withdraw Options
class ViewClassesFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='#ffffff')

        label = tk.Label(self, text="View Classes", font=("Arial", 64, "bold"), bg="#ffffff", fg="#ff0000")
        label.pack(pady=10, anchor='center')

        self.classes_label = tk.Label(self, text="", font=("Arial", 18), bg="#ffffff")
        self.classes_label.pack(pady=10, anchor='center')

        # Member ID Entry
        tk.Label(self, text="Member ID:", font=("Arial", 24), bg="#ffffff").pack(pady=5, anchor='center')
        self.member_id_entry = tk.Entry(self, width=20)
        self.member_id_entry.pack(pady=5, anchor='center')

        # Dropdown to select class
        tk.Label(self, text="Select Class:", font=("Arial", 24), bg="#ffffff").pack(pady=5, anchor='center')
        self.selected_class = tk.StringVar(self)
        self.selected_class.set("Yoga")  # Default value
        class_options = tk.OptionMenu(self, self.selected_class, *self.controller.classes.keys())
        class_options.pack(pady=10, anchor='center')

        # Sign Up and Withdraw Buttons
        sign_up_button = tk.Button(self, text="Sign Up", command=self.sign_up_member, bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        sign_up_button.pack(pady=5, anchor='center')

        withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw_member, bg="#ff0000", fg="#ffffff", font=("Arial", 24))
        withdraw_button.pack(pady=5, anchor='center')

        self.display_classes()

        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), bg="#cccccc", font=("Arial", 24))
        back_button.pack(pady=20, anchor='center')

    def display_classes(self):
        class_info = ""
        for class_name, class_obj in self.controller.classes.items():
            enrolled_members = [m.name for m in class_obj.enrolled_members]
            class_info += f"{class_name} Class:\nInstructor: {class_obj.instructor}\nTime: {class_obj.time}\nEnrolled Members: {', '.join(enrolled_members)}\n\n"
        self.classes_label.config(text=class_info)

    def sign_up_member(self):
        member_id = self.member_id_entry.get()
        selected_class = self.selected_class.get()
        member = next((m for m in self.controller.members if m.member_id == member_id), None)
    
        if member:
            # Check if the member is already enrolled in the selected class
            if member in self.controller.classes[selected_class].enrolled_members:
                messagebox.showinfo("Duplicate Enrollment", f"{member.name} is already signed up for {selected_class}.")
            else:
                self.controller.classes[selected_class].enroll_member(member)
                messagebox.showinfo("Sign Up", f"{member.name} has successfully signed up for {selected_class}.")
                self.display_classes()
        else:
            messagebox.showwarning("Sign Up", "Member not found. Please enroll first.")
    def withdraw_member(self):
        member_id = self.member_id_entry.get()
        selected_class = self.selected_class.get()
        member = next((m for m in self.controller.members if m.member_id == member_id), None)
    
        if member:
            # Check if the member is enrolled in the selected class
            if member in self.controller.classes[selected_class].enrolled_members:
                self.controller.classes[selected_class].enrolled_members.remove(member)
                messagebox.showinfo("Withdraw", f"{member.name} has successfully withdrawn from {selected_class}.")
                self.display_classes()
            else:
                messagebox.showwarning("Withdraw", f"{member.name} is not currently enrolled in {selected_class}.")
        else:
            messagebox.showwarning("Withdraw", "Member not found. Please enroll first.")


# Run the app
if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()
