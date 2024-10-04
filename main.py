import json  # Import the json module for handling configuration data stored in JSON format.
import re  # Import the re module for handling regular expressions.
import tkinter as tk  # Import the tkinter module for creating the GUI components.
from PIL import Image, ImageTk  # Import the Pillow library for image manipulation and Tkinter compatibility.
from tkinter import messagebox  # Import the messagebox module from tkinter for displaying message dialogs.
from members import Member  # Import the Member class from the members module (custom class for member management).
from classes import ClassSchedule  # Import the ClassSchedule class from the classes module (custom class for class scheduling).
from notifications import Notification  # Import the Notification class from the notifications module (custom class for notifications).

# Function to load configuration settings from a JSON file.
def load_config():
    with open('config.json', 'r') as f:  # Open the 'config.json' file in read mode.
        config = json.load(f)  # Load the configuration data into a dictionary.
    return config  # Return the loaded configuration.

# Define the main application class for the fitness app, inheriting from the Tkinter root class (tk.Tk).
class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()  # Initialize the parent Tk class.
        self.title("Cardinal Fitness Check-In System")  # Set the application title.
        self.configure(bg='#ffffff')  # Set the background color for the app.

        self.attributes('-fullscreen', True)  # Start the application in fullscreen mode.

        self.bind("<Escape>", self.exit_fullscreen)  # Bind the 'Escape' key to exit fullscreen mode.

        self.config = load_config()  # Load the configuration settings.
        self.default_capacity = self.config['default_class_capacity']  # Set the default class capacity from config.
        self.default_notification_message = self.config['notification_message']  # Set the default notification message.

        self.members = []  # Initialize an empty list to hold the members.
        # Initialize class schedules with sample classes.
        self.classes = {
            "Yoga": ClassSchedule("C001", "Yoga", "Alice Johnson", "10:00 AM", self.default_capacity),
            "Spinning": ClassSchedule("C002", "Spinning", "John Doe", "12:00 PM", self.default_capacity),
        }

        self.frames = {}  # Dictionary to hold the different frames (pages) of the application.
        self.create_frames()  # Call the method to create all frames (pages).

        self.show_frame("MainMenu")  # Show the main menu frame by default.

    # Method to create and configure all the frames/pages of the application.
    def create_frames(self):
        for F in (MainMenu, CheckInFrame, EnrollFrame, ViewClassesFrame):  # Iterate through the different frame classes.
            page_name = F.__name__  # Get the class name as the page name.
            frame = F(parent=self, controller=self)  # Create an instance of the frame.
            self.frames[page_name] = frame  # Add the frame to the frames dictionary.
            frame.grid(row=0, column=0, sticky="nsew")  # Use grid layout to position the frame.

        self.grid_rowconfigure(0, weight=1)  # Configure row stretching to fill available space.
        self.grid_columnconfigure(0, weight=1)  # Configure column stretching to fill available space.

    # Method to display a specific frame based on the frame name.
    def show_frame(self, page_name):
        frame = self.frames[page_name]  # Retrieve the frame instance from the frames dictionary.
        frame.tkraise()  # Raise the frame to the top of the stacking order to display it.

    # Method to exit the fullscreen mode.
    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)  # Disable the fullscreen attribute.

# Define the Main Menu frame class, inheriting from the Tkinter Frame class (tk.Frame).
class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # Initialize the parent Frame class.
        self.controller = controller  # Set the controller reference to access the main application.
        self.configure(bg='#ffffff')  # Set the background color for the frame.

        self.logo_image = None  # Placeholder for storing the loaded logo image.
        self.logo_photo = None  # Placeholder for storing the processed image for display.

        self.load_logo_image()  # Load the logo image.

        # Create and configure the main title label.
        title_label = tk.Label(self, text="Cardinal Fitness", font=("Arial", 64, "bold"), bg="#232323", fg="#ff0000")
        title_label.pack(anchor='n', fill='x', expand=True)  # Position and style the title label.

        # Define a common button style dictionary for the main menu buttons.
        button_style = {"font": ("Arial", 24, "bold"), "bg": "#ff0000", "fg": "#ffffff", "activebackground": "#d40000", "cursor": "hand2", "relief": "flat"}

        # Create and position the Check In/Checkout button.
        check_in_button = tk.Button(self, text="Check In/Checkout", command=lambda: controller.show_frame("CheckInFrame"), **button_style)
        check_in_button.place(anchor='center', relx=0.5, rely=0.35)

        # Create and position the Enroll Member button.
        enroll_button = tk.Button(self, text="Enroll Member", command=lambda: controller.show_frame("EnrollFrame"),  **button_style)
        enroll_button.place(anchor='center', relx=0.5, rely=0.5)

        # Create and position the View Classes button.
        view_classes_button = tk.Button(self, text="View Classes", command=lambda: controller.show_frame("ViewClassesFrame"),  **button_style)
        view_classes_button.place(anchor='center', relx=0.5, rely=0.65)

        self.bind("<Configure>", self.on_resize)  # Bind the 'Configure' event to handle resizing of the frame.

    # Method to load the logo image from a specified file path.
    def load_logo_image(self):
        try:
            image_path = "C:/Users/david/OneDrive/Desktop/Cardinal Fitness/assets/Cardinal Fitness Logo.png"  # Define the image file path.

            self.logo_image = Image.open(image_path)  # Open the image file using Pillow.

            self.logo_label = tk.Label(self, bg='#ffffff')  # Create a label widget to display the image.
            self.logo_label.place(relx=0.5, rely=0.5, anchor='center')  # Position the label at the center.

        except Exception as e:  # Handle exceptions if the image fails to load.
            print(f"Error displaying the logo image: {e}")  # Print the error message to the console.

    # Method to update the logo image based on the current frame size.
    def update_logo_image(self):
        frame_height = self.winfo_height()  # Get the current height of the frame.
        frame_width = self.winfo_width()  # Get the current width of the frame.

        if frame_height > 0 and frame_width > 0 and self.logo_image:  # Ensure valid dimensions and image are available.
            aspect_ratio = self.logo_image.width / self.logo_image.height  # Calculate the aspect ratio of the image.
            new_height = int(frame_height)  # Set the new height based on the frame height.
            new_width = int(new_height * aspect_ratio)  # Calculate the new width to maintain aspect ratio.

            if new_width > 0 and new_height > 0:  # Check if the new dimensions are valid.
                resized_image = self.logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image using high-quality resampling.
                self.logo_photo = ImageTk.PhotoImage(resized_image)  # Convert the image to a format compatible with Tkinter.

                self.logo_label.config(image=self.logo_photo)  # Update the label to display the resized image.
                self.logo_label.image = self.logo_photo  # Prevent image garbage collection by retaining a reference.

    # Event handler method to trigger image updates when the frame is resized.
    def on_resize(self, event):
        self.update_logo_image()  # Call the method to update the logo image.
# Define the CheckInFrame class for handling the member check-in/check-out functionality.
class CheckInFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # Initialize the parent Frame class.
        self.controller = controller  # Set the controller reference to access the main application.
        self.configure(bg='#ffffff')  # Set the background color for the frame.

        self.logo_image = None  # Placeholder for storing the loaded logo image.
        self.logo_photo = None  # Placeholder for storing the processed image for display.

        self.load_logo_image()  # Load the logo image.

        # Define a common button style dictionary for the buttons used in this frame.
        button_style = {
            "font": ("Arial", 24, "bold"),  # Set font style and size.
            "bg": "#ff0000",  # Set button background color.
            "fg": "#ffffff",  # Set button text color.
            "activebackground": "#d40000",  # Set active state background color.
            "activeforeground": "#ffffff",  # Set active state text color.
            "cursor": "hand2",  # Change cursor to hand on hover.
            "relief": "flat",  # Remove button border.
            "bd": 0  # Set border width to 0.
        }
        
        # Define a common entry style dictionary for the text entry widget used for member ID input.
        entry_style = {
            "font": ("Arial", 24),  # Set font style and size.
            "bd": 2,  # Set border width.
            "relief": "solid",  # Set border style to solid.
            "bg": "#ffffff",  # Set background color.
            "fg": "#333333",  # Set text color.
            "insertbackground": "#ff0000",  # Set the color of the insertion cursor.
            "highlightbackground": "#ff0000",  # Set border color when not focused.
            "highlightcolor": "#ff0000",  # Set border color when focused.
            "highlightthickness": 1,  # Set border thickness.
            "width": 30  # Set the width of the entry box.
        }

        # Create and configure the main title label for the Check-In/Check-Out frame.
        title_label = tk.Label(self, text="Member Check In/Check Out", font=("Arial", 64, "bold"), bg="#232323", fg="#ff0000")
        title_label.pack(anchor='n', fill='x', expand=True)  # Position and style the title label.

        # Create the member ID entry field.
        self.member_id_entry = tk.Entry(self, **entry_style)  # Apply the entry style to the Entry widget.
        self.member_id_entry.place(anchor='center', relx=0.5, rely=0.25)  # Position the entry widget at the top-center.

        # Create and position the Check In button.
        check_in_button = tk.Button(self, text="Check In", command=self.check_in_member, **button_style)  # Apply the button style.
        check_in_button.place(anchor='center', relx=0.5, rely=0.35)  # Position the button.

        # Create and position the Check Out button.
        check_out_button = tk.Button(self, text="Check Out", command=self.check_out_member, **button_style)  # Apply the button style.
        check_out_button.place(anchor='center', relx=0.5, rely=0.5)  # Position the button.

        # Create and position the Back to Main Menu button.
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), **button_style)  # Apply the button style.
        back_button.place(anchor='center', relx=0.5, rely=0.65)  # Position the button.

        self.bind("<Configure>", self.on_resize)  # Bind the 'Configure' event to handle resizing of the frame.

    # Method to load the logo image from a specified file path.
    def load_logo_image(self):
        try:
            image_path = "C:/Users/david/OneDrive/Desktop/Cardinal Fitness/assets/Cardinal Fitness Logo.png"  # Define the image file path.

            self.logo_image = Image.open(image_path)  # Open the image file using Pillow.

            self.logo_label = tk.Label(self, bg='#ffffff')  # Create a label widget to display the image.
            self.logo_label.place(relx=0.5, rely=0.5, anchor='center')  # Position the label at the center.

        except Exception as e:  # Handle exceptions if the image fails to load.
            print(f"Error displaying the logo image: {e}")  # Print the error message to the console.

    # Method to update the logo image based on the current frame size.
    def update_logo_image(self):
        frame_height = self.winfo_height()  # Get the current height of the frame.
        frame_width = self.winfo_width()  # Get the current width of the frame.

        if frame_height > 0 and frame_width > 0 and self.logo_image:  # Ensure valid dimensions and image are available.
            aspect_ratio = self.logo_image.width / self.logo_image.height  # Calculate the aspect ratio of the image.
            new_height = int(frame_height)  # Set the new height based on the frame height.
            new_width = int(new_height * aspect_ratio)  # Calculate the new width to maintain aspect ratio.

            if new_width > 0 and new_height > 0:  # Check if the new dimensions are valid.
                resized_image = self.logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image using high-quality resampling.
                self.logo_photo = ImageTk.PhotoImage(resized_image)  # Convert the image to a format compatible with Tkinter.

                self.logo_label.config(image=self.logo_photo)  # Update the label to display the resized image.
                self.logo_label.image = self.logo_photo  # Prevent image garbage collection by retaining a reference.

    # Event handler method to trigger image updates when the frame is resized.
    def on_resize(self, event):
        self.update_logo_image()  # Call the method to update the logo image.

    # Method to handle member check-in logic.
    def check_in_member(self):
        member_id = self.member_id_entry.get()  # Get the member ID from the entry widget.
        member = next((m for m in self.controller.members if m.member_id == member_id), None)  # Find the member by ID.

        if member:  # Check if the member exists.
            if member.checked_in:  # Check if the member is already checked in.
                messagebox.showinfo("Already Checked In", f"{member.name}, you are already checked in.")  # Show a message.
            else:
                member.check_in()  # Mark the member as checked in.
                messagebox.showinfo("Check In", f"{member.name} has successfully checked in.")  # Show a success message.
        else:
            messagebox.showwarning("Check In", "Member not found. Please enroll first.")  # Show a warning if the member is not found.

    # Method to handle member check-out logic.
    def check_out_member(self):
        member_id = self.member_id_entry.get()  # Get the member ID from the entry widget.
        member = next((m for m in self.controller.members if m.member_id == member_id), None)  # Find the member by ID.

        if member:  # Check if the member exists.
            if not member.checked_in:  # Check if the member is already checked out.
                messagebox.showinfo("Already Checked Out", f"{member.name}, you are already checked out.")  # Show a message.
            else:
                member.check_out()  # Mark the member as checked out.
                messagebox.showinfo("Check Out", f"{member.name} has successfully checked out.")  # Show a success message.
        else:
            messagebox.showwarning("Check Out", "Member not found. Please enroll first.")  # Show a warning if the member is not found.
# Define the EnrollFrame class for handling member enrollment functionality.
class EnrollFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # Initialize the parent Frame class.
        self.controller = controller  # Set the controller reference to access the main application.
        self.configure(bg='#ffffff')  # Set the background color for the frame.

        self.logo_image = None  # Placeholder for storing the loaded logo image.
        self.logo_photo = None  # Placeholder for storing the processed image for display.

        self.load_logo_image()  # Load the logo image.

        # Define a common button style dictionary for the buttons used in this frame.
        button_style = {
            "font": ("Arial", 24, "bold"),  # Set font style and size.
            "bg": "#ff0000",  # Set button background color.
            "fg": "#ffffff",  # Set button text color.
            "activebackground": "#d40000",  # Set active state background color.
            "activeforeground": "#ffffff",  # Set active state text color.
            "cursor": "hand2",  # Change cursor to hand on hover.
            "relief": "flat",  # Remove button border.
            "bd": 0  # Set border width to 0.
        }
        
        # Define a common entry style dictionary for the text entry widgets used in this frame.
        entry_style = {
            "font": ("Arial", 24),  # Set font style and size.
            "bd": 2,  # Set border width.
            "relief": "solid",  # Set border style to solid.
            "bg": "#ffffff",  # Set background color.
            "fg": "#333333",  # Set text color.
            "insertbackground": "#ff0000",  # Set the color of the insertion cursor.
            "highlightbackground": "#ff0000",  # Set border color when not focused.
            "highlightcolor": "#ff0000",  # Set border color when focused.
            "highlightthickness": 1,  # Set border thickness.
            "width": 30  # Set the width of the entry box.
        }

        # Define a common label style dictionary for the labels used in this frame.
        label_style = {
            "font": ("Arial", 24, "bold"),  # Set font style and size.
            "bg": "#232323",  # Set background color.
            "fg": "#ffffff",  # Set text color.
            "anchor": "w",  # Set anchor position for text alignment.
            "padx": 10,  # Set padding for text within the label.
        }

        # Create and configure the main title label for the Enroll Member frame.
        title_label = tk.Label(self, text="Enroll Member", font=("Arial", 64, "bold"), bg="#232323", fg="#ff0000")
        title_label.pack(anchor='n', fill='x', expand=True)  # Position and style the title label.

        # Create and position the label and entry for the Member Name field.
        tk.Label(self, text="Member Name:", **label_style).place(anchor='center', relx=0.5, rely=0.2)
        self.member_name_entry = tk.Entry(self, **entry_style)  # Apply the entry style to the Entry widget.
        self.member_name_entry.place(anchor='center', relx=0.5, rely=0.25)

        # Create and position the label and entry for the Email field.
        tk.Label(self, text="Email:", **label_style).place(anchor='center', relx=0.5, rely=0.3)
        self.member_email_entry = tk.Entry(self, **entry_style)  # Apply the entry style to the Entry widget.
        self.member_email_entry.place(anchor='center', relx=0.5, rely=0.35)

        # Create and position the Enroll button.
        enroll_button = tk.Button(self, text="Enroll", command=self.enroll_member, **button_style)  # Apply the button style.
        enroll_button.place(anchor='center', relx=0.5, rely=0.5)  # Position the button.

        # Create and position the Back to Main Menu button.
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), **button_style)  # Apply the button style.
        back_button.place(anchor='center', relx=0.5, rely=0.65)  # Position the button.

        self.bind("<Configure>", self.on_resize)  # Bind the 'Configure' event to handle resizing of the frame.

    # Method to load the logo image from a specified file path.
    def load_logo_image(self):
        try:
            image_path = "C:/Users/david/OneDrive/Desktop/Cardinal Fitness/assets/Cardinal Fitness Logo.png"  # Define the image file path.

            self.logo_image = Image.open(image_path)  # Open the image file using Pillow.

            self.logo_label = tk.Label(self, bg='#ffffff')  # Create a label widget to display the image.
            self.logo_label.place(relx=0.5, rely=0.5, anchor='center')  # Position the label at the center.

        except Exception as e:  # Handle exceptions if the image fails to load.
            print(f"Error displaying the logo image: {e}")  # Print the error message to the console.

    # Method to update the logo image based on the current frame size.
    def update_logo_image(self):
        frame_height = self.winfo_height()  # Get the current height of the frame.
        frame_width = self.winfo_width()  # Get the current width of the frame.

        if frame_height > 0 and frame_width > 0 and self.logo_image:  # Ensure valid dimensions and image are available.
            aspect_ratio = self.logo_image.width / self.logo_image.height  # Calculate the aspect ratio of the image.
            new_height = int(frame_height)  # Set the new height based on the frame height.
            new_width = int(new_height * aspect_ratio)  # Calculate the new width to maintain aspect ratio.

            if new_width > 0 and new_height > 0:  # Check if the new dimensions are valid.
                resized_image = self.logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image using high-quality resampling.
                self.logo_photo = ImageTk.PhotoImage(resized_image)  # Convert the image to a format compatible with Tkinter.

                self.logo_label.config(image=self.logo_photo)  # Update the label to display the resized image.
                self.logo_label.image = self.logo_photo  # Prevent image garbage collection by retaining a reference.

    # Event handler method to trigger image updates when the frame is resized.
    def on_resize(self, event):
        self.update_logo_image()  # Call the method to update the logo image.

    # Method to handle member enrollment logic.
    def enroll_member(self):
        member_name = self.member_name_entry.get()  # Get the member name from the entry widget.
        member_email = self.member_email_entry.get()  # Get the member email from the entry widget.
    
        # Define a helper function to validate email format using a regular expression.
        def is_valid_email(email):
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'  # Regular expression for valid email.
            return re.match(email_regex, email) is not None  # Return True if the email matches the pattern.

        if not is_valid_email(member_email):  # Check if the email is not valid.
            messagebox.showwarning("Invalid Email", "Please enter a valid email address.")  # Show a warning message.
            return  # Exit the method early if the email is invalid.

        for member in self.controller.members:  # Iterate through existing members to check for duplicate emails.
            if member.email == member_email:  # Check if the email is already in use.
                messagebox.showwarning("Duplicate Email", "This email is already in use. Please use a different email.")  # Show a warning message.
                return  # Exit the method early if a duplicate is found.

        if member_name and member_email:  # Check if both fields are filled out.
            new_member_id = f"M{len(self.controller.members) + 1:03d}"  # Generate a new unique member ID.
            new_member = Member(new_member_id, member_name, member_email)  # Create a new Member instance.
            self.controller.members.append(new_member)  # Add the new member to the controller's member list.

            notification = Notification(self.controller.default_notification_message, new_member)  # Create a new notification instance.
            notification.send_notification()  # Send a notification for the new member enrollment.

            messagebox.showinfo("Enrollment", f"{new_member.name} has been enrolled in the gym with ID: {new_member_id}.")  # Show a success message.
        else:
            messagebox.showwarning("Enrollment", "Please fill out both fields.")  # Show a warning if any field is empty.
# Define the ViewClassesFrame class for displaying and managing class enrollments.
class ViewClassesFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)  # Initialize the parent Frame class.
        self.controller = controller  # Set the controller reference to access the main application.
        self.configure(bg='#ffffff')  # Set the background color for the frame.

        self.logo_image = None  # Placeholder for storing the loaded logo image.
        self.logo_photo = None  # Placeholder for storing the processed image for display.

        self.load_logo_image()  # Load the logo image.

        # Define a common button style dictionary for the buttons used in this frame.
        button_style = {
            "font": ("Arial", 24, "bold"),  # Set font style and size.
            "bg": "#ff0000",  # Set button background color.
            "fg": "#ffffff",  # Set button text color.
            "activebackground": "#d40000",  # Set active state background color.
            "activeforeground": "#ffffff",  # Set active state text color.
            "cursor": "hand2",  # Change cursor to hand on hover.
            "relief": "flat",  # Remove button border.
            "bd": 0  # Set border width to 0.
        }
        
        # Define a common entry style dictionary for the text entry widgets used in this frame.
        entry_style = {
            "font": ("Arial", 24),  # Set font style and size.
            "bd": 2,  # Set border width.
            "relief": "solid",  # Set border style to solid.
            "bg": "#ffffff",  # Set background color.
            "fg": "#333333",  # Set text color.
            "insertbackground": "#ff0000",  # Set the color of the insertion cursor.
            "highlightbackground": "#ff0000",  # Set border color when not focused.
            "highlightcolor": "#ff0000",  # Set border color when focused.
            "highlightthickness": 1,  # Set border thickness.
            "width": 30  # Set the width of the entry box.
        }

        # Define a common label style dictionary for the labels used in this frame.
        label_style = {
            "font": ("Arial", 24),  # Set font style and size.
            "bg": "#232323",  # Set background color.
            "fg": "#ffffff",  # Set text color.
            "anchor": "w",  # Set anchor position for text alignment.
            "padx": 10,  # Set padding for text within the label.
        }

        # Create and configure the main title label for the View Classes frame.
        title_label = tk.Label(self, text="View Classes", font=("Arial", 64, "bold"), bg="#232323", fg="#ff0000")
        title_label.pack(anchor='n', fill='x')  # Position and style the title label.

        # Create and configure the label to display class details.
        self.classes_label = tk.Label(self, text="", **label_style)  # Apply the label style.
        self.classes_label.pack(pady=10, anchor='center')  # Position the label at the center.

        # Create and configure the Member ID label and entry.
        tk.Label(self, text="Member ID:", **label_style).pack(pady=5, anchor='center')  # Position the label.
        self.member_id_entry = tk.Entry(self, **entry_style)  # Apply the entry style to the Entry widget.
        self.member_id_entry.pack(pady=5, anchor='center')  # Position the entry widget.

        # Create and configure the Select Class label and dropdown.
        tk.Label(self, text="Select Class:", **label_style).pack(pady=5, anchor='center')  # Position the label.
        self.selected_class = tk.StringVar(self)  # Define a StringVar to hold the selected class.
        self.selected_class.set("Yoga")  # Set the default value for the dropdown.
        class_options = tk.OptionMenu(self, self.selected_class, *self.controller.classes.keys())  # Create the dropdown menu.
        class_options.pack(pady=10, anchor='center')  # Position the dropdown menu.

        # Create and position the Sign Up button.
        sign_up_button = tk.Button(self, text="Sign Up", command=self.sign_up_member, **button_style)  # Apply the button style.
        sign_up_button.pack(pady=5, anchor='center')  # Position the button.

        # Create and position the Withdraw button.
        withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw_member, **button_style)  # Apply the button style.
        withdraw_button.pack(pady=5, anchor='center')  # Position the button.

        self.display_classes()  # Display the class details.

        # Create and position the Back to Main Menu button.
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame("MainMenu"), **button_style)  # Apply the button style.
        back_button.pack(pady=20, anchor='center')  # Position the button.

        self.bind("<Configure>", self.on_resize)  # Bind the 'Configure' event to handle resizing of the frame.

    # Method to load the logo image from a specified file path.
    def load_logo_image(self):
        try:
            image_path = "C:/Users/david/OneDrive/Desktop/Cardinal Fitness/assets/Cardinal Fitness Logo.png"  # Define the image file path.

            self.logo_image = Image.open(image_path)  # Open the image file using Pillow.

            self.logo_label = tk.Label(self, bg='#ffffff')  # Create a label widget to display the image.
            self.logo_label.place(relx=0.5, rely=0.5, anchor='center')  # Position the label at the center.

        except Exception as e:  # Handle exceptions if the image fails to load.
            print(f"Error displaying the logo image: {e}")  # Print the error message to the console.

    # Method to update the logo image based on the current frame size.
    def update_logo_image(self):
        frame_height = self.winfo_height()  # Get the current height of the frame.
        frame_width = self.winfo_width()  # Get the current width of the frame.

        if frame_height > 0 and frame_width > 0 and self.logo_image:  # Ensure valid dimensions and image are available.
            aspect_ratio = self.logo_image.width / self.logo_image.height  # Calculate the aspect ratio of the image.
            new_height = int(frame_height)  # Set the new height based on the frame height.
            new_width = int(new_height * aspect_ratio)  # Calculate the new width to maintain aspect ratio.

            if new_width > 0 and new_height > 0:  # Check if the new dimensions are valid.
                resized_image = self.logo_image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resize the image using high-quality resampling.
                self.logo_photo = ImageTk.PhotoImage(resized_image)  # Convert the image to a format compatible with Tkinter.

                self.logo_label.config(image=self.logo_photo)  # Update the label to display the resized image.
                self.logo_label.image = self.logo_photo  # Prevent image garbage collection by retaining a reference.

    # Event handler method to trigger image updates when the frame is resized.
    def on_resize(self, event):
        self.update_logo_image()  # Call the method to update the logo image.

    # Method to display the details of all classes.
    def display_classes(self):
        class_info = ""  # Initialize an empty string to hold class information.
        for class_name, class_obj in self.controller.classes.items():  # Iterate through all classes.
            enrolled_members = [m.name for m in class_obj.enrolled_members]  # Get the names of enrolled members.
            # Format and add class details to the class_info string.
            class_info += f"{class_name} Class:\nInstructor: {class_obj.instructor}\nTime: {class_obj.time}\nEnrolled Members: {', '.join(enrolled_members)}\n\n"
        self.classes_label.config(text=class_info)  # Update the label to display the formatted class information.

    # Method to sign up a member for a class.
    def sign_up_member(self):
        member_id = self.member_id_entry.get()  # Get the member ID from the entry widget.
        selected_class = self.selected_class.get()  # Get the selected class from the dropdown.
        member = next((m for m in self.controller.members if m.member_id == member_id), None)  # Find the member by ID.

        if member:  # Check if the member exists.
            class_schedule = self.controller.classes[selected_class]  # Get the class schedule for the selected class.
        
            if member in class_schedule.enrolled_members:  # Check if the member is already enrolled.
                messagebox.showinfo("Duplicate Enrollment", f"{member.name} is already signed up for {selected_class}.")  # Show a message.
            else:
                if len(class_schedule.enrolled_members) < class_schedule.capacity:  # Check if the class is not full.
                    class_schedule.enroll_member(member)  # Enroll the member in the class.
                    messagebox.showinfo("Sign Up", f"{member.name} has successfully signed up for {selected_class}.")  # Show a success message.
                else:
                    messagebox.showwarning("Class Full", f"Sorry, the {selected_class} class is full.")  # Show a warning if the class is full.

                self.display_classes()  # Update the class display.
        else:
            messagebox.showwarning("Sign Up", "Member not found. Please enroll first.")  # Show a warning if the member is not found.

    # Method to withdraw a member from a class.
    def withdraw_member(self):
        member_id = self.member_id_entry.get()  # Get the member ID from the entry widget.
        selected_class = self.selected_class.get()  # Get the selected class from the dropdown.
        member = next((m for m in self.controller.members if m.member_id == member_id), None)  # Find the member by ID.
    
        if member:  # Check if the member exists.
            if member in self.controller.classes[selected_class].enrolled_members:  # Check if the member is enrolled in the class.
                self.controller.classes[selected_class].enrolled_members.remove(member)  # Remove the member from the enrolled members list.
                messagebox.showinfo("Withdraw", f"{member.name} has successfully withdrawn from {selected_class}.")  # Show a success message.
                self.display_classes()  # Update the class display.
            else:
                messagebox.showwarning("Withdraw", f"{member.name} is not currently enrolled in {selected_class}.")  # Show a warning if not enrolled.
        else:
            messagebox.showwarning("Withdraw", "Member not found. Please enroll first.")  # Show a warning if the member is not found.

# The main entry point of the application.
if __name__ == "__main__":
    app = FitnessApp()  # Create an instance of the FitnessApp class.
    app.mainloop()  # Start the main event loop, which waits for user interaction and updates the GUI.

