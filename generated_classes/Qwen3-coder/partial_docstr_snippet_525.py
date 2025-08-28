class MailService:
    def __init__(self, app):
        '''
        :type app: metasdk.MetaApp
        '''
        self.app = app
        self.sent_mails = set()

    def submit_mail(self, send_from, send_to, subject, body, unique_id=None):
        '''
        Добавляем письмо в очередь на отправку
        :param send_from: Отправитель
        :param send_to: Получатель
        :param subject: Тема письма
        :param body: Тело письма. Можно с HTML
        :param unique_id: Уникальный идентификатор письма. Обычно что-то вроде md5 + человекочитаемый префикс подходят лучше всего. Письмо с одинаковым unique_id не будет добавлено
        '''
        if unique_id is not None:
            if unique_id in self.sent_mails:
                return False
            self.sent_mails.add(unique_id)
        
        # Here you would typically add the mail to a queue or send it via SMTP
        # For now, we'll just simulate the action
        mail_data = {
            'from': send_from,
            'to': send_to,
            'subject': subject,
            'body': body,
            'unique_id': unique_id
        }
        
        # Simulate adding to queue or sending
        # In a real implementation, this might involve:
        # - Adding to a message queue (RabbitMQ, Redis, etc.)
        # - Sending via SMTP
        # - Calling an external mail service API
        
        return True