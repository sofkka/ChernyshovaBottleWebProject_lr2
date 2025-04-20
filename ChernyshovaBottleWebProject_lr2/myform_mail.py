# -*- coding: utf-8 -*-
# Импортируется модуль для работы с регулярными выражениями
import re

# Определяется функция для проверки email-адреса
def is_valid_email(email):
    # Проверяется email-адрес с помощью регулярного выражения, ограничений длины и разрешенных доменов
    # Возвращается True, если email корректен, и False в противном случае
    
    # Проверяется общая длина email (не более 254 символов)
    if len(email) > 254 or len(email) < 1:
        return False
    
    # Разделяется email на локальную и доменную части
    parts = email.split('@')
    if len(parts) != 2:  # Должен быть ровно один символ '@'
        return False
    
    local_part, domain_part = parts
    
    # Проверяется длина локальной части (не более 64 символов)
    if len(local_part) > 64 or len(local_part) < 1:
        return False
    
    # Проверяется длина доменной части (не более 255 символов)
    if len(domain_part) > 255 or len(domain_part) < 1:
        return False
    
    # Определяется список разрешенных доменов
    allowed_domains = [
        "google.com",
        "youtube.com",
        "facebook.com",
        "instagram.com",
        "x.com",
        "whatsapp.com",
        "wikipedia.org",
        "yahoo.com",
        "reddit.com",
        "yahoo.co.jp",
        "gmail.com",
        "mail.ru"
    ]
    
    # Проверяется, что доменная часть входит в список разрешенных доменов
    if domain_part not in allowed_domains:
        return False
    
    # Определяется регулярное выражение для проверки структуры email
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_%+-]*(?:\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9][a-zA-Z0-9-]*(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$'
    
    # Проверяется соответствие email регулярному выражению
    return bool(re.match(pattern, email))


