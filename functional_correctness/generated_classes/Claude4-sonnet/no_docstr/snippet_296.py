class Email:
    def __init__(self, data, manager):
        self.data = data
        self.manager = manager
        self.id = data.get('id')
        self.subject = data.get('subject', '')
        self.sender = data.get('sender', '')
        self.recipient = data.get('recipient', '')
        self.body = data.get('body', '')
        self.timestamp = data.get('timestamp')
        self.read = data.get('read', False)

    def update(self):
        if self.manager and hasattr(self.manager, 'update_email'):
            self.manager.update_email(self)
        else:
            for key, value in self.__dict__.items():
                if key not in ['manager', 'data']:
                    self.data[key] = value

    def delete(self):
        if self.manager and hasattr(self.manager, 'delete_email'):
            self.manager.delete_email(self)

    def __str__(self):
        return f"From: {self.sender}\nTo: {self.recipient}\nSubject: {self.subject}\n\n{self.body}"

    def __repr__(self):
        return f"Email(id={self.id}, subject='{self.subject}', sender='{self.sender}', recipient='{self.recipient}')"