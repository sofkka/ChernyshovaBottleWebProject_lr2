from bottle import post, request
import re
from datetime import datetime
import pdb
import json
import os

# словарь для хранения вопросов (email -> question)
email_and_question = {}

# список допустимых доменов
ALLOWED_DOMAINS = ['gmail.com', 'yandex.ru', 'mail.ru', 'yahoo.com', 'outlook.com']

DATA_FILE = "data.txt"

# загрузка данных из файла
def load_data():
    # если файл существует
    if os.path.exists(DATA_FILE):
        # используем оператор with для безопасной работы с файлом
        with open(DATA_FILE, 'r') as f:     # 'r' - режим чтения
            # пытаемся загрузить JSON-данные из файла
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # в случае ошибки декодирования JSON возвращаем пустой словарь
                return {}
    # если файл не существует, возвращаем пустой словарь
    return {}

# сохранение данных в файл
def save_data(data):
    # используем оператор with для безопасной работы с файлом
    with open(DATA_FILE, 'w') as f:
        # в параметрах - данные для сохранения, файл для записи, форматирование с отступами, сохранение символов Unicode нетронутыми
        json.dump(data, f, indent=4, ensure_ascii=False)


@post('/home', method='post')
def my_form():
    # получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # проверка на заполнение всех полей
    if not email or not username or not question:
        return "Please fill in all fields!"

    # проверка длины имени (не более 64 символов)
    if len(username) > 64:
        return "Username should be no more than 64 characters!"

    # проверка длины почты (не более 254 символов)
    if len(email) > 254:
        return "Email should be no more than 254 characters!"

    # проверка длины вопроса (не более 1000 символов)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

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

    # проверка, что вопрос не состоит из одних цифр
    if question.isdigit():
        return "Question should not consist of digits only!"

    # проверка, что вопрос состоит минимум из 3 букв
    if not re.search(r'[a-zA-Z]{3,}', question):
        return "Question must contain at least 3 Latin letters!"

    # записываем данные в словарь в виде списка [username, question]
    email_and_question[email] = [username, question]
    
    # точка останова для отладки
    pdb.set_trace()

    # загружаем существующие данные
    data = load_data()

    # если данные для введенной ПОЧТЫ УЖЕ ЕСТЬ, проверяем их структуру
    if email in data:
        # Если данные старого формата ([username, question]), преобразуем в новый формат
        if isinstance(data[email], list):
            # извлекаем имя пользователя и вопрос из списка
            old_username, old_question = data[email]
            # создаем новую структуру данных для этой почты
            data[email] = {
                'username': old_username,
                'questions': [old_question]
            }
    
    # инициализация записи для пользователя, если нет такой ПОЧТЫ
    if email not in data:
        data[email] = {
            'username': username,
            'questions': []
        }

    # проверка на дубликаты ВОПРОСА
    if question not in data[email]['questions']:
        data[email]['questions'].append(question)
    else:
        return "You've already asked this question!"

    # обновляем имя пользователя
    data[email]['username'] = username

    # сохраняем данные
    save_data(data)

    # получение текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")

    # формирование результирующего сообщения
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message
