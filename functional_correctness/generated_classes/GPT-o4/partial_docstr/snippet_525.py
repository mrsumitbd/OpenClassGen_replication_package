class MailService:
    def __init__(self, app):
        """
            :type app: metasdk.MetaApp
        """
        self.app = app
        self._coll = app.db['mail_queue']
        self._coll.create_index('unique_id', unique=True, sparse=True)

    def submit_mail(self, send_from, send_to, subject, body, unique_id=None):
        """
            Добавляем письмо в очередь на отправку
            :param send_from: Отправитель
            :param send_to: Получатель
            :param subject: Тема письма
            :param body: Тело письма. Можно с HTML
            :param unique_id: Уникальный идентификатор письма. Обычно что-то вроде md5 + человекочитаемый префикс подходят лучше всего. Письмо с одинаковым unique_id не будет добавлено
        """
        doc = {
            'send_from': send_from,
            'send_to': send_to,
            'subject': subject,
            'body': body,
            'created_at': datetime.utcnow()
        }
        if unique_id is not None:
            doc['unique_id'] = unique_id
        try:
            result = self._coll.insert_one(doc)
        except DuplicateKeyError:
            return
        return result.inserted_id