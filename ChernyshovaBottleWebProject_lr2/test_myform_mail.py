# -*- coding: utf-8 -*-
# ������������� ������ unittest ��� �������� � ������� ������
import unittest
# ������������� ������ myform_mail � �������� �������� email
import myform_mail

# ������������ ����� ��� ������������, ����������� �� unittest.TestCase
class TestEmailValidation(unittest.TestCase):
    # ������������ ����� ��� �������� ���������� email-�������
    def test_valid_emails(self):
        # ��������� ������ ���������� email-�������
        list_mail_cor = [
            "m.m@mail.ru",
            "m1@gmail.com",
            "sofya.cher@youtube.com",
            "test.user@facebook.com",
            "sofya.cher123@instagram.com",
            "sofya_cher@x.com",
            "sofya+cher@whatsapp.com",
            "sofya@wikipedia.org",
            "sofya.cher@yahoo.com",
            "123sof@reddit.com",
            "Sofya@yahoo.co.jp",
            "SOFYA@google.com",
            "123@mail.ru"
        ]
        # ������������ email-������ �� ������
        for email in list_mail_cor:
            # �����������, ��� ������� is_valid_email ���������� True
            self.assertTrue(
                myform_mail.is_valid_email(email),
                f"Was expected that {email} must be a valid email"
                )

    # ������������ ����� ��� �������� ������������ email-�������
    def test_invalid_emails(self):
        # ��������� email � ��������� ������ ������� 64 ��������
        long_local = "s" * 65 + "@mail.ru"
        # ��������� email � �������� ������ ������� 255 ��������
        long_domain = "user@" + "s" * 250 + ".com"
        # ��������� ������ ������������ email-�������
        list_mail_uncor = [
            # ������ ������
            "",
            # ���� ������
            "1",
            # ����������� �����
            "m1@",
            # ����������� ��� ������������
            "@mail",
            # ����������� ��� ������
            "s1@.ru",
            # ����������� ����� �������� ������
            "s1@mail",
            # �������� ����� �������� ������
            "s1@mail.",
            # ������� ����� � ����� ������������
            "s1..ofya@mail.ru",
            # ����� � ������ ������
            "s1@.mail.ru",
            # ������� ����� � ������
            "s1@mail..ru",
            # ������ � ����� ������������
            "s1 probel@mail.ru",
            # ��������� �������� @
            "s1@of@mail.ru",
            # ��������� ����� ������� 64 ��������
            long_local,
            # �������� ����� ������� 255 ��������
            long_domain,
            # ����� ������� �����
            "s" * 100 + "@" + "s" * 150 + ".ru",
            # ��� ������������ ���������� � �����
            ".s1@mail.ru",
            # ������� �������� ����� �������� ������
            "m1@mail.c",
            # ������������������ �������������
            "______@mail.ru",
            # �������������� �����
            "sofya@outlook.com",
            # �������������� �����
            "user@yandex.ru"
        ]
        # ������������ email-������ �� ������
        for email in list_mail_uncor:
            # �����������, ��� ������� is_valid_email ���������� False
            self.assertFalse(
                myform_mail.is_valid_email(email),
                f"Was expected that {email} must be an invalid email"
                )

# �����������, ����������� �� ������ ��������
if __name__ == '__main__':
    # ����������� ��� �����
    unittest.main()
