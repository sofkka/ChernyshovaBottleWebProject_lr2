from bottle import post, request, response
import re
from datetime import datetime

# список допустимых доменов
ALLOWED_DOMAINS = ['gmail.com', 'vk.com', 'mail.ru', 'yahoo.com', 'outlook.com']

@post('/home', method='post')
def my_form():

    # получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # проверка на заполнение всех полей
    if not email or not username or not question:
        return "Please fill in all fields!"

    # проверка длины имени (не более 15 символов)
    if len(username) > 15:
        return "Username should be no more than 15 characters!"

    # проверка длины почты (не более 15 символов)
    if len(email) > 15:
        return "Email should be no more than 15 characters!"

    # проверка длины вопроса (не более 200 символов)
    if len(question) > 200:
        return "Question should be no more than 200 characters!"

    # проверка длины вопроса (не менее 5 символов)
    if len(question) < 5:
        return "Question should be more than 5 characters!"

    # проверка имени: только латинские буквы, без цифр и других символов
    if not re.match(r'^[a-zA-Z]+$', username):
        return "Username should contain only Latin letters!"

    # проверка, что почта не начинается с цифры
    if email and email[0].isdigit():
        return "Email should not start with a digit!"

    # проверка формата email и допустимых доменов
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Incorrect email format! Please change your address!"

    # проверка, что домен email находится в списке допустимых
    domain = email.split('@')[1]
    if domain not in ALLOWED_DOMAINS:
        return f"Email domain '{domain}' is not allowed. Please use one of the following: {', '.join(ALLOWED_DOMAINS)}"

    # проверка, что email не содержит запрещенных символов (только латинские буквы, цифры, точки, подчеркивания, дефисы)
    if not re.match(r'^[a-zA-Z0-9_.+-]+$', email.split('@')[0]):
        return "Email contains invalid characters. Please use only Latin letters, numbers, dots, underscores, and hyphens."

    # получение текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")

    # формирование результирующего сообщения
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"

    return result_message
