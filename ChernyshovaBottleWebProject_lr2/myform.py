# -*- coding: cp1251 -*-
from bottle import post, request
import re
from datetime import datetime
import pdb
import json
import os
from myform_mail import is_valid_email

DATA_FILE = "data.json"

# �������� ������ �� �����
def load_data():
    # ���� ���� ����������
    if os.path.exists(DATA_FILE):
        # ���������� �������� with ��� ���������� ������ � ������
        with open(DATA_FILE, 'r', encoding='utf-8') as f:     # 'r' - ����� ������
            # �������� ��������� JSON-������ �� �����
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # � ������ ������ ������������� JSON ���������� ������ �������
                return {}
    # ���� ���� �� ����������, ���������� ������ �������
    return {}

# ���������� ������ � ����
def save_data(data):
    # ���������� �������� with ��� ���������� ������ � ������
    with open(DATA_FILE, 'w') as f:
        # � ���������� - ������ ��� ����������, ���� ��� ������, �������������� � ���������, ���������� �������� Unicode �����������
        json.dump(data, f, indent=4, ensure_ascii=False)


@post('/home', method='post')
def my_form():
    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # ����������� ���������� ���� �����
    if not email or not username or not question:
        return "Please fill in all fields!"

    # ����������� ����� ����� (�� ����� 64 ��������)
    if len(username) > 64:
        return "Username should be no more than 64 characters!"

    # ����������� ����� ������� (�� ����� 1000 ��������)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

    # ����������� ���: ������ ��������� �����, ��� ���� � ������ ��������
    if not re.match(r'^[a-zA-Z]+$', username):
        return "Username should contain only Latin letters!"

    # ����������� ������ email � ������� ������� is_valid_email
    if not is_valid_email(email):
        allowed_domains = ["google.com", "youtube.com", "facebook.com", "instagram.com",
                           "x.com", "whatsapp.com", "wikipedia.org", "yahoo.com",
                           "reddit.com", "gmail.com", "mail.ru"]
        return f"Incorrect email format or domain! Please use one of the following domains: {', '.join(allowed_domains)}"

    # �����������, ��� ������ �� ������� �� ����� ����
    if question.isdigit():
        return "Question should not consist of digits only!"

    # �����������, ��� ������ �������� ������� 3 �����
    if not re.search(r'[a-zA-Z]{3,}', question):
        return "Question must contain at least 3 Latin letters!"
    
    # ��������������� ����� �������� ��� �������
    # pdb.set_trace()

    # ����������� ������������ ������
    data = load_data()

    # ����������� ��������� ������ ��� email
    if email in data:
        # ������������� ������ ������ � �����
        if isinstance(data[email], list):
            old_username, old_question = data[email]
            data[email] = {
                'username': old_username,
                'questions': [old_question]
            }
    
    # ���������������� ������ ��� ������ email
    if email not in data:
        data[email] = {
            'username': username,
            'questions': []
        }

    # ����������� �������� �������
    if question not in data[email]['questions']:
        data[email]['questions'].append(question)
    else:
        return "You've already asked this question!"

    # ����������� ��� ������������
    data[email]['username'] = username

    # ����������� ������
    save_data(data)

    # ���������� ������� ����
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ����������� ��������� �� �������� ���������
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message
