from bottle import post, request, response
import re
from datetime import datetime

@post('/home', method='post')
def my_form():

    # получение данных из формы
    question = request.forms.get('QUEST', '').strip()
    username = request.forms.get('USERNAME', '').strip()
    email = request.forms.get('ADRESS', '').strip()

    if not email or not username or not question:
        return "Please fill in all fields!"

    # проверка формата email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Incorrect email format! Please change your adress!"

    # получение текущей даты
    current_date = datetime.now().strftime("%Y-%m-%d")

    # формирование результирующего сообщения
    result_message = f"Thanks, {username}! <br>The answer will be sent to the email {email}. <br>Access Date: {current_date}"

    return result_message
