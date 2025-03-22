from bottle import post, request, response
import re
from datetime import datetime

# ������ ���������� �������
ALLOWED_DOMAINS = ['gmail.com', 'vk.com', 'mail.ru', 'yahoo.com', 'outlook.com']

@post('/home', method='post')
def my_form():

    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # �������� �� ���������� ���� �����
    if not email or not username or not question:
        return "Please fill in all fields!"

    # �������� ����� ����� (�� ����� 15 ��������)
    if len(username) > 15:
        return "Username should be no more than 15 characters!"

    # �������� ����� ����� (�� ����� 15 ��������)
    if len(email) > 15:
        return "Email should be no more than 15 characters!"

    # �������� ����� ������� (�� ����� 200 ��������)
    if len(question) > 200:
        return "Question should be no more than 200 characters!"

    # �������� ����� ������� (�� ����� 5 ��������)
    if len(question) < 5:
        return "Question should be more than 5 characters!"

    # �������� �����: ������ ��������� �����, ��� ���� � ������ ��������
    if not re.match(r'^[a-zA-Z]+$', username):
        return "Username should contain only Latin letters!"

    # ��������, ��� ����� �� ���������� � �����
    if email and email[0].isdigit():
        return "Email should not start with a digit!"

    # �������� ������� email � ���������� �������
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Incorrect email format! Please change your address!"

    # ��������, ��� ����� email ��������� � ������ ����������
    domain = email.split('@')[1]
    if domain not in ALLOWED_DOMAINS:
        return f"Email domain '{domain}' is not allowed. Please use one of the following: {', '.join(ALLOWED_DOMAINS)}"

    # ��������, ��� email �� �������� ����������� �������� (������ ��������� �����, �����, �����, �������������, ������)
    if not re.match(r'^[a-zA-Z0-9_.+-]+$', email.split('@')[0]):
        return "Email contains invalid characters. Please use only Latin letters, numbers, dots, underscores, and hyphens."

    # ��������� ������� ����
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ������������ ��������������� ���������
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"

    return result_message
