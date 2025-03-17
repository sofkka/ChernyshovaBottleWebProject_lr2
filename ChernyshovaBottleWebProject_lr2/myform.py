from bottle import post, request, response
import re
from datetime import datetime

@post('/home', method='post')
def my_form():

    # ��������� ������ �� �����
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    if not email or not username or not question:
        return "Please fill in all fields!"

    # �������� ������� email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Incorrect email format! Please change your adress!"

    # ��������� ������� ����
    current_date = datetime.now().strftime("%Y-%m-%d")

    # ������������ ��������������� ���������
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"

    return result_message
