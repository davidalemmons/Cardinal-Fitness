# Define the Notification class to manage and send notifications to gym members.
class Notification:
    def __init__(self, message, member):
        # Initialize the notification with the provided message and member.
        self.message = message  # The notification message to be sent.
        self.member = member  # The member to whom the notification will be sent.

    # Method to send the notification.
    def send_notification(self):
        # Print a formatted message indicating the notification has been sent.
        print(f"Notification sent to {self.member.name}: {self.message}")
