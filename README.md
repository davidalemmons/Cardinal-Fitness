#Cardinal Fitness Check-In System
##Overview
The Cardinal Fitness Check-In System is a desktop-based application designed to streamline member check-ins, class enrollments, and schedule management for gyms and fitness centers. The application uses a Tkinter-based GUI and integrates various Python modules to deliver a comprehensive user experience for fitness administrators and members.

##Features
##Member Check-In and Check-Out: 
Allows members to check in and out of the gym using their unique member ID.
##Member Enrollment: 
New members can be enrolled using their name and email. The system verifies unique emails to avoid duplicates.
##Class Management: 
Schedule classes with defined capacities, instructors, and timings. Supports member enrollments and withdrawals for each class.
##GUI-Based Interaction: 
User-friendly interface built using Python's Tkinter library.
##Notification System:
 Notifies users of successful check-ins, enrollments, and any errors during interactions.
##Data Configuration:
Easily configurable settings via a config.json file, allowing custom class capacities and notification messages.
Project Structure
##main.py: 
Entry point of the application. Contains the main logic for navigation and screen management.
##members.py: 
Contains the Member class for handling member attributes and interactions.
##classes.py: 
Contains the ClassSchedule class for managing class attributes, scheduling, and enrollment.
##notifications.py: 
Implements the Notification class for sending notifications during specific events.
##config.json: 
Configuration file for defining default class capacities and notification messages.
##README.md: 
Project documentation.
##assets/: 
Contains the logo and any other images used in the interface.
##Installation
##Prerequisites
##Python 3.8 or higher
##Required libraries:
tkinter
Pillow (Python Imaging Library)
##Setup
1. Clone the repository:git clone https://github.com/username/CardinalFitness.git
2. Navigate to the project directory: cd CardinalFitness
3. Install required dependencies: pip install -r requirements.txt
4. Run the application: python main.py
##Configuration
Modify config.json to change the default class capacity or notification messages.
Update image paths and assets in the assets/ folder if customizing the UI.
Usage
Navigation
##Main Menu:
 From the main menu, users can choose to:
Check In / Check Out
Enroll a new Member
View Classes and manage class enrollments.
Check In / Check Out: Users input their member ID to register their presence.
##Enroll Member: 
Users provide their name and a unique email address to create a new membership.
##View Classes: 
Admins can view the class schedules, enroll members, and withdraw members from classes.
Future Enhancements
Add user authentication for better security.
Implement reporting and analytics for attendance tracking.
Cloud-based data storage for multi-device support.
License
This project is licensed under the MIT License.

Author
David Lemmons