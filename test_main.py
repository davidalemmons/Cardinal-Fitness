import unittest
from unittest.mock import patch, MagicMock
from main import FitnessApp
from members import Member
from classes import ClassSchedule
from notifications import Notification

class TestFitnessApp(unittest.TestCase):

    @patch("main.load_config")
    def setUp(self, mock_load_config):
        # Mock configuration
        mock_load_config.return_value = {
            "default_class_capacity": 10,
            "notification_message": "Welcome to Cardinal Fitness!"
        }
        # Initialize the FitnessApp
        self.app = FitnessApp()
        self.app.withdraw()  # Prevent the Tkinter window from actually opening during tests

    def test_initialization(self):
        self.assertEqual(self.app.default_capacity, 10)
        self.assertEqual(self.app.default_notification_message, "Welcome to Cardinal Fitness!")

    def test_show_frame(self):
        # Show the MainMenu frame
        self.app.show_frame("MainMenu")
        # Check that MainMenu is currently at the top (shown)
        self.assertEqual(self.app.frames["MainMenu"].winfo_manager(), "grid")


    def test_exit_fullscreen(self):
        with patch.object(self.app, 'attributes') as mock_attributes:
            self.app.exit_fullscreen()
            mock_attributes.assert_called_with('-fullscreen', False)

    def test_member_check_in(self):
        # Create a mock member and add to the app's member list
        member = Member("M001", "John Doe", "john@example.com")
        self.app.members.append(member)

        # Check in the member using the method in CheckInFrame
        self.app.frames['CheckInFrame'].member_id_entry.insert(0, "M001")
        with patch("tkinter.messagebox.showinfo"):
            self.app.frames['CheckInFrame'].check_in_member()
        self.assertTrue(member.checked_in)

    def test_member_check_out(self):
        member = Member("M001", "John Doe", "john@example.com")
        member.check_in()  # Mark member as checked in
        self.app.members.append(member)

        # Check out the member using the method in CheckInFrame
        self.app.frames['CheckInFrame'].member_id_entry.insert(0, "M001")
        with patch("tkinter.messagebox.showinfo"):
            self.app.frames['CheckInFrame'].check_out_member()
        self.assertFalse(member.checked_in)

    def test_enroll_member(self):
        # Simulate user input
        self.app.frames['EnrollFrame'].member_name_entry.insert(0, "Jane Smith")
        self.app.frames['EnrollFrame'].member_email_entry.insert(0, "jane@example.com")

        with patch("tkinter.messagebox.showinfo"), patch("tkinter.messagebox.showwarning"):
            self.app.frames['EnrollFrame'].enroll_member()

        # Check if the new member was added
        self.assertEqual(len(self.app.members), 1)
        self.assertEqual(self.app.members[0].name, "Jane Smith")
        self.assertEqual(self.app.members[0].email, "jane@example.com")

    def test_invalid_email_enrollment(self):
        self.app.frames['EnrollFrame'].member_name_entry.insert(0, "Jane Smith")
        self.app.frames['EnrollFrame'].member_email_entry.insert(0, "invalid-email")

        with patch("tkinter.messagebox.showwarning") as mock_warning:
            self.app.frames['EnrollFrame'].enroll_member()
            mock_warning.assert_called_with("Invalid Email", "Please enter a valid email address.")

    def test_class_enrollment(self):
        member = Member("M001", "John Doe", "john@example.com")
        self.app.members.append(member)

        # Select Yoga class and enter member ID
        self.app.frames['ViewClassesFrame'].member_id_entry.insert(0, "M001")
        self.app.frames['ViewClassesFrame'].selected_class.set("Yoga")

        with patch("tkinter.messagebox.showinfo"):
            self.app.frames['ViewClassesFrame'].sign_up_member()
        
        # Check if the member is enrolled
        self.assertIn(member, self.app.classes["Yoga"].enrolled_members)

    def test_class_withdrawal(self):
        member = Member("M001", "John Doe", "john@example.com")
        self.app.members.append(member)
        self.app.classes["Yoga"].enroll_member(member)

        # Select Yoga class and enter member ID
        self.app.frames['ViewClassesFrame'].member_id_entry.insert(0, "M001")
        self.app.frames['ViewClassesFrame'].selected_class.set("Yoga")

        with patch("tkinter.messagebox.showinfo"):
            self.app.frames['ViewClassesFrame'].withdraw_member()

        # Check if the member is no longer enrolled
        self.assertNotIn(member, self.app.classes["Yoga"].enrolled_members)

if __name__ == '__main__':
    unittest.main()
