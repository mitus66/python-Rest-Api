from mongoengine import Document, StringField, DateTimeField, ReferenceField, ListField, BooleanField

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField() # Зберігаємо як рядок, як у JSON
    born_location = StringField()
    description = StringField()

    meta = {'collection': 'authors'} # Явно вказуємо назву колекції

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return f"Author(fullname='{self.fullname}')"

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True) # Поле-посилання на Author
    quote = StringField(required=True)

    meta = {'collection': 'quotes'} # Явно вказуємо назву колекції

    def __str__(self):
        return f'"{self.quote}" - {self.author.fullname}'

    def __repr__(self):
        return f"Quote(author='{self.author.fullname}', quote='{self.quote[:30]}...')"

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone_number = StringField() # Додано поле для телефонного номера
    address = StringField()
    is_sent = BooleanField(default=False) # Поле для відстеження статусу відправки email
    # Додано поле для кращого способу надсилання, з вибором з 'email' або 'sms'
    preferred_method = StringField(choices=['email', 'sms'], default='email')

    meta = {'collection': 'contacts'} # Явно вказуємо назву колекції

    def __str__(self):
        return f"Contact: {self.fullname} <{self.email}> (Phone: {self.phone_number}, Preferred: {self.preferred_method}, Sent: {self.is_sent})"

    def __repr__(self):
        return f"Contact(fullname='{self.fullname}', email='{self.email}', phone='{self.phone_number}', preferred='{self.preferred_method}', is_sent={self.is_sent})"
