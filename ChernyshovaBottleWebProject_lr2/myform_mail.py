# -*- coding: utf-8 -*-
# ������������� ������ ��� ������ � ����������� �����������
import re

# ������������ ������� ��� �������� email-������
def is_valid_email(email):
    # ����������� email-����� � ������� ����������� ���������, ����������� ����� � ����������� �������
    # ������������ True, ���� email ���������, � False � ��������� ������
    
    # ����������� ����� ����� email (�� ����� 254 ��������)
    if len(email) > 254 or len(email) < 1:
        return False
    
    # ����������� email �� ��������� � �������� �����
    parts = email.split('@')
    if len(parts) != 2:  # ������ ���� ����� ���� ������ '@'
        return False
    
    local_part, domain_part = parts
    
    # ����������� ����� ��������� ����� (�� ����� 64 ��������)
    if len(local_part) > 64 or len(local_part) < 1:
        return False
    
    # ����������� ����� �������� ����� (�� ����� 255 ��������)
    if len(domain_part) > 255 or len(domain_part) < 1:
        return False
    
    # ������������ ������ ����������� �������
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
    
    # �����������, ��� �������� ����� ������ � ������ ����������� �������
    if domain_part not in allowed_domains:
        return False
    
    # ������������ ���������� ��������� ��� �������� ��������� email
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9_%+-]*(?:\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9][a-zA-Z0-9-]*(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$'
    
    # ����������� ������������ email ����������� ���������
    return bool(re.match(pattern, email))


