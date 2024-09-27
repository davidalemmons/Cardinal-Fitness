# notifications.py
class Notification:
    def __init__(self, message, member):
        self.message = message
        self.member = member

    def send_notification(self):
        # Mock notification functionality for now
        print(f"Notification sent to {self.member.name}: {self.message}")

