class Email:
    def __init__(self, data, manager):
        self.data = data
        self.manager = manager
        self.id = data.get('id')
        self.sender = data.get('sender')
        self.recipient = data.get('recipient')
        self.subject = data.get('subject')
        self.body = data.get('body')
        self.timestamp = data.get('timestamp')
        self.is_read = data.get('is_read', False)

    def update(self):
        if self.manager and self.id:
            self.manager.update_email(self.id, self.data)

    def delete(self):
        if self.manager and self.id:
            self.manager.delete_email(self.id)
            self.id = None

    def __str__(self):
        return f"Email from {self.sender} to {self.recipient}: {self.subject}"

    def __repr__(self):
        return f"Email(id={self.id}, sender='{self.sender}', recipient='{self.recipient}', subject='{self.subject}')"