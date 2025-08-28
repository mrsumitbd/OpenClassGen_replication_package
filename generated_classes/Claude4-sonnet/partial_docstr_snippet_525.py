class MailService:
    def __init__(self, app):
        '''
        :type app: metasdk.MetaApp
        '''
        self.app = app
        self.mail_queue = []
        self.sent_unique_ids = set()

    def submit_mail(self, send_from, send_to, subject, body, unique_id=None):
        '''
        Добавляем письмо в очередь на отправку
        :param send_from: Отправитель
        :param send_to: Получатель
        :param subject: Тема письма
        :param body: Тело письма. Можно с HTML
        :param unique_id: Уникальный идентификатор письма. Обычно что-то вроде md5 + человекочитаемый префикс подходят лучше всего. Письмо с одинаковым unique_id не будет добавлено
        '''
        if unique_id is None:
            unique_id = hashlib.md5(f"{send_from}{send_to}{subject}{body}{time.time()}".encode()).hexdigest()
        
        if unique_id in self.sent_unique_ids:
            return False
        
        mail_data = {
            'send_from': send_from,
            'send_to': send_to,
            'subject': subject,
            'body': body,
            'unique_id': unique_id
        }
        
        self.mail_queue.append(mail_data)
        self.sent_unique_ids.add(unique_id)
        return True