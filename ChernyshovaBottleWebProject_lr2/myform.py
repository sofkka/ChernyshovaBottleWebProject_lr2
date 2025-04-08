from bottle import post, request
import re
from datetime import datetime
import pdb
import json
import os

# ������� ��� �������� �������� (email -> question)
email_and_question = {}

# ������ ���������� �������
ALLOWED_DOMAINS = ['gmail.com', 'yandex.ru', 'mail.ru', 'yahoo.com', 'outlook.com']

DATA_FILE = "data.txt"

# �������� ������ �� �����
def load_data():
    # ���� ���� ����������
    if os.path.exists(DATA_FILE):
        # ���������� �������� with ��� ���������� ������ � ������
        with open(DATA_FILE, 'r') as f:     # 'r' - ����� ������
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

    # �������� �� ���������� ���� �����
    if not email or not username or not question:
        return "Please fill in all fields!"

    # �������� ����� ����� (�� ����� 64 ��������)
    if len(username) > 64:
        return "Username should be no more than 64 characters!"

    # �������� ����� ����� (�� ����� 254 ��������)
    if len(email) > 254:
        return "Email should be no more than 254 characters!"

    # �������� ����� ������� (�� ����� 1000 ��������)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

    # �������� �����: ������ ��������� �����, ��� ���� � ������ ��������
    if not re.match(r'^[a-zA-Z]+$', username):
        return "Username should contain only Latin letters!"

    # ��������, ��� ����� �� ���������� � �����
    if email and email[0].isdigit():
        return "Email should not start with a digit!"

    # �������� ������� email � ���������� �������
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-z]+\.[a-z]+$', email):
        return f"Incorrect email format! Please change your address! Please use one of the following domains: {', '.join(ALLOWED_DOMAINS)}"

    # ��������, ��� ����� email ��������� � ������ ����������
    domain = email.split('@')[1]
    if domain not in ALLOWED_DOMAINS:
        return f"Email domain '{domain}' is not allowed. Please use one of the following: {', '.join(ALLOWED_DOMAINS)}"

    # ��������, ��� ������ �� ������� �� ����� ����
    if question.isdigit():
        return "Question should not consist of digits only!"

    # ��������, ��� ������ ������� ������� �� 3 ����
    if not re.search(r'[a-zA-Z]{3,}', question):
        return "Question must contain at least 3 Latin letters!"

    # ���������� ������ � ������� � ���� ������ [username, question]
    email_and_question[email] = [username, question]
    
    # ����� �������� ��� �������
    pdb.set_trace()

    # ��������� ������������ ������
    data = load_data()

    # ���� ������ ��� ��������� ����� ��� ����, ��������� �� ���������
    if email in data:
        # ���� ������ ������� ������� ([username, question]), ����������� � ����� ������
        if isinstance(data[email], list):
            # ��������� ��� ������������ � ������ �� ������
            old_username, old_question = data[email]
            # ������� ����� ��������� ������ ��� ���� �����
            data[email] = {
                'username': old_username,
                'questions': [old_question]
            }
    
    # ������������� ������ ��� ������������, ���� ��� ����� �����
    if email not in data:
        data[email] = {
            'username': username,
            'questions': []
        }

    # �������� �� ��������� �������
    if question not in data[email]['questions']:
        data[email]['questions'].append(question)
    else:
        return "You've already asked this question!"

    # ��������� ��� ������������
    data[email]['username'] = username

    # ��������� ������
    save_data(data)

    # ��������� ������� ����
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ������������ ��������������� ���������
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message
