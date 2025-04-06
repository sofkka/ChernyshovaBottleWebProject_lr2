from bottle import post, request, response
import re
from datetime import datetime
import pdb  # ����������� ������ ��� �������

# ������� ��� �������� �������� (email -> question)
email_and_question = {}

# ������ ���������� �������
ALLOWED_DOMAINS = ['gmail.com', 'yandex.ru', 'mail.ru', 'yahoo.com', 'outlook.com']

# ������� ���������� POST-������ �� /home
@post('/home', method='post')
def my_form():
    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    # �������� �� ���������� ���� �����
    if not email or not username or not question:
        return "Please fill in all fields!"

    # �������� ����� ����� (�� ����� 25 ��������)
    if len(username) > 25:
        return "Username should be no more than 25 characters!"

    # �������� ����� ����� (�� ����� 254 ��������)
    if len(email) > 254:
        return "Email should be no more than 254 characters!"

    # �������� ����� ������� (�� ����� 1000 ��������)
    if len(question) > 1000:
        return "Question should be no more than 1000 characters!"

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
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-z]+\.[a-z]+$', email):
        return f"Incorrect email format! Please change your address! Please use one of the following domains: {', '.join(ALLOWED_DOMAINS)}"

    # ��������, ��� ����� email ��������� � ������ ����������
    domain = email.split('@')[1]
    if domain not in ALLOWED_DOMAINS:
        return f"Email domain '{domain}' is not allowed. Please use one of the following: {', '.join(ALLOWED_DOMAINS)}"
    
    # ���������� ������ � ������� � ���� ������ [username, question]
    list1 = [username, question]
    email_and_question[email] = list1
    
    # ����� �������� ��� �������
    pdb.set_trace()

    # ��������� ������� ����
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ������������ ��������������� ���������
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"
    
    return result_message