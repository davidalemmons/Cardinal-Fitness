# Import necessary modules for testing.
import unittest  # Unittest framework for creating and running tests.
import re  # Regular expression module for email validation.
from members import Member  # Import the Member class from the members module.
from classes import ClassSchedule  # Import the ClassSchedule class from the classes module.
from main import load_config  # Import the load_config function from the main module.

# Test suite for testing member functionality.
class TestMemberFunctionality(unittest.TestCase):

    # Set up the initial conditions for each test case.
    def setUp(self):
        self.member1 = Member("M001", "John Doe", "johndoe@example.com")  # Create a sample member.
        self.member2 = Member("M002", "Jane Smith", "janesmith@example.com")  # Create another sample member.
        self.class_yoga = ClassSchedule("C001", "Yoga", "Alice Johnson", "10:00 AM", 5)  # Create a sample class with capacity 5.

    # Test for member check-in and check-out functionality.
    def test_member_check_in_out(self):
        self.assertFalse(self.member1.checked_in)  # Verify the member is not checked in initially.
        
        self.member1.check_in()  # Check in the member.
        self.assertTrue(self.member1.checked_in)  # Verify the member is now checked in.

        self.member1.check_out()  # Check out the member.
        self.assertFalse(self.member1.checked_in)  # Verify the member is now checked out.

    # Test to verify that two members cannot have duplicate emails.
    def test_member_duplicate_email(self):
        member_duplicate = Member("M003", "Duplicate", "johndoe@example.com")  # Create a member with duplicate email.
        
        self.assertEqual(self.member1.email, member_duplicate.email)  # Check that emails are equal.

    # Test for enrolling members into a class.
    def test_class_enrollment(self):
        self.class_yoga.enroll_member(self.member1)  # Enroll the first member in the class.
        self.class_yoga.enroll_member(self.member2)  # Enroll the second member in the class.
        
        self.assertIn(self.member1, self.class_yoga.enrolled_members)  # Verify the first member is in the enrolled list.
        self.assertIn(self.member2, self.class_yoga.enrolled_members)  # Verify the second member is in the enrolled list.
        
        self.assertEqual(len(self.class_yoga.enrolled_members), 2)  # Verify the total number of enrolled members.

    # Test for handling class capacity limits.
    def test_class_capacity(self):
        for i in range(self.class_yoga.capacity):  # Loop to fill the class to its maximum capacity.
            new_member = Member(f"M{i+3:03d}", f"Member {i+3}", f"member{i+3}@example.com")  # Create new members.
            self.class_yoga.enroll_member(new_member)  # Enroll each member.

        extra_member = Member("M008", "Overflow Member", "overflow@example.com")  # Create an extra member.
        self.class_yoga.enroll_member(extra_member)  # Attempt to enroll the extra member.
        
        self.assertNotIn(extra_member, self.class_yoga.enrolled_members)  # Verify the extra member is not enrolled.

    # Test for loading configuration from a file.
    def test_load_config(self):
        config = load_config()  # Load the configuration.
        self.assertIsInstance(config, dict)  # Verify that the configuration is a dictionary.
        self.assertIn('default_class_capacity', config)  # Check for the 'default_class_capacity' key.
        self.assertIn('notification_message', config)  # Check for the 'notification_message' key.
        self.assertGreaterEqual(config['default_class_capacity'], 1)  # Verify the capacity is at least 1.

# Test suite for validating email addresses.
class TestValidations(unittest.TestCase):
    # Test for valid email addresses.
    def test_valid_email(self):
        valid_emails = [
            "test@example.com",
            "user.name+tag+sorting@example.com",
            "x@example.com",  # One-letter local-part.
            "example-indeed@strange-example.com"
        ]
        for email in valid_emails:
            self.assertTrue(self.is_valid_email(email))  # Verify that each email is valid.

    # Test for invalid email addresses.
    def test_invalid_email(self):
        invalid_emails = [
            "plainaddress",  # Missing @ symbol and domain.
            "@missingusername.com",  # Missing username.
            "user@.nodomain",  # Missing domain.
            "user@invalid-characters-in-domain!",  # Invalid characters in domain.
            "user@domain..com"  # Double dot in domain.
        ]
        for email in invalid_emails:
            self.assertFalse(self.is_valid_email(email))  # Verify that each email is invalid.

    # Helper method to validate email format using a regular expression.
    @staticmethod
    def is_valid_email(email):
        email_regex = r"^(?!\.)[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"  # Regular expression for valid emails.
        return bool(re.match(email_regex, email)) and '..' not in email  # Return True if email matches and has no double dots.

# Main entry point to run the test cases.
if __name__ == "__main__":
    unittest.main()  # Run all the test cases in the file.
