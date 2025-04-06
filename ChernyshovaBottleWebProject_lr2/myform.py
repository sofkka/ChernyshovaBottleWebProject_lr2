from bottle import post, request, response
import re
from datetime import datetime
import pdb  # импортируем модуль для отладки

# словарь для хранения вопросов (email -> question)
email_and_question = {}

# список допустимых доменов
ALLOWED_DOMAINS = ['gmail.com', 'yandex.ru', 'mail.ru', 'yahoo.com', 'outlook.com']

# браузер отправляет POST-запрос на /home
@post('/home', method='post')
def my_form():
    # получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # проверка на заполнение всех полей
    if not email or not username or not question:
        return "Please fill in all fields!"

    # проверка длины имени (не более 25 символов)
    if len(username) > 25:
        return "Username should be no more than 25 characters!"

    # проверка длины почты (не более 254 символов)
    if len(email) > 254:
        return "Email should be no more than 254 characters!"

    # проверка длины вопроса (не более 1000 символов)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

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
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-z]+\.[a-z]+$', email):
        return f"Incorrect email format! Please change your address! Please use one of the following domains: {', '.join(ALLOWED_DOMAINS)}"

    # проверка, что домен email находится в списке допустимых
    domain = email.split('@')[1]
    if domain not in ALLOWED_DOMAINS:
        return f"Email domain '{domain}' is not allowed. Please use one of the following: {', '.join(ALLOWED_DOMAINS)}"
    
    # записываем данные в словарь в виде списка [username, question]
    list1 = [username, question]
    email_and_question[email] = list1
    
    # точка останова для отладки
    pdb.set_trace()

    # получение текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")

    # формирование результирующего сообщения
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message