# -*- coding: cp1251 -*-
from bottle import post, request
import re
from datetime import datetime
import pdb
import json
import os
from myform_mail import is_valid_email

DATA_FILE = "data.json"

# загрузка данных из файла
def load_data():
    # если файл существует
    if os.path.exists(DATA_FILE):
        # используем оператор with для безопасной работы с файлом
        with open(DATA_FILE, 'r', encoding='utf-8') as f:     # 'r' - режим чтения
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

    # Проверяется заполнение всех полей
    if not email or not username or not question:
        return "Please fill in all fields!"

    # Проверяется длина имени (не более 64 символов)
    if len(username) > 64:
        return "Username should be no more than 64 characters!"

    # Проверяется длина вопроса (не более 1000 символов)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

    # Проверяется имя: только латинские буквы, без цифр и других символов
    if not re.match(r'^[a-zA-Z]+$', username):
        return "Username should contain only Latin letters!"

    # Проверяется формат email с помощью функции is_valid_email
    if not is_valid_email(email):
        allowed_domains = ["google.com", "youtube.com", "facebook.com", "instagram.com",
                           "x.com", "whatsapp.com", "wikipedia.org", "yahoo.com",
                           "reddit.com", "gmail.com", "mail.ru"]
        return f"Incorrect email format or domain! Please use one of the following domains: {', '.join(allowed_domains)}"

    # Проверяется, что вопрос не состоит из одних цифр
    if question.isdigit():
        return "Question should not consist of digits only!"

    # Проверяется, что вопрос содержит минимум 3 буквы
    if not re.search(r'[a-zA-Z]{3,}', question):
        return "Question must contain at least 3 Latin letters!"
    
    # Устанавливается точка останова для отладки
    # pdb.set_trace()

    # Загружаются существующие данные
    data = load_data()

    # Проверяется структура данных для email
    if email in data:
        # Преобразуется старый формат в новый
        if isinstance(data[email], list):
            old_username, old_question = data[email]
            data[email] = {
                'username': old_username,
                'questions': [old_question]
            }
    
    # Инициализируется запись для нового email
    if email not in data:
        data[email] = {
            'username': username,
            'questions': []
        }

    # Проверяется дубликат вопроса
    if question not in data[email]['questions']:
        data[email]['questions'].append(question)
    else:
        return "You've already asked this question!"

    # Обновляется имя пользователя
    data[email]['username'] = username

    # Сохраняются данные
    save_data(data)

    # Получается текущая дата
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Формируется сообщение об успешной обработке
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message
