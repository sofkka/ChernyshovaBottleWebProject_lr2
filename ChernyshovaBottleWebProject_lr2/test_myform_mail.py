# -*- coding: utf-8 -*-
# Импортируется модуль unittest для создания и запуска тестов
import unittest
# Импортируется модуль myform_mail с функцией проверки email
import myform_mail

# Определяется класс для тестирования, наследуемый от unittest.TestCase
class TestEmailValidation(unittest.TestCase):
    # Определяется метод для проверки корректных email-адресов
    def test_valid_emails(self):
        # Создается список корректных email-адресов
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
        # Перебираются email-адреса из списка
        for email in list_mail_cor:
            # Проверяется, что функция is_valid_email возвращает True
            self.assertTrue(
                myform_mail.is_valid_email(email),
                f"Was expected that {email} must be a valid email"
                )

    # Определяется метод для проверки некорректных email-адресов
    def test_invalid_emails(self):
        # Создается email с локальной частью длиннее 64 символов
        long_local = "s" * 65 + "@mail.ru"
        # Создается email с доменной частью длиннее 255 символов
        long_domain = "user@" + "s" * 250 + ".com"
        # Создается список некорректных email-адресов
        list_mail_uncor = [
            # Пустая строка
            "",
            # Один символ
            "1",
            # Отсутствует домен
            "m1@",
            # Отсутствует имя пользователя
            "@mail",
            # Отсутствует имя домена
            "s1@.ru",
            # Отсутствует домен верхнего уровня
            "s1@mail",
            # Неполный домен верхнего уровня
            "s1@mail.",
            # Двойная точка в имени пользователя
            "s1..ofya@mail.ru",
            # Точка в начале домена
            "s1@.mail.ru",
            # Двойная точка в домене
            "s1@mail..ru",
            # Пробел в имени пользователя
            "s1 probel@mail.ru",
            # Несколько символов @
            "s1@of@mail.ru",
            # Локальная часть длиннее 64 символов
            long_local,
            # Доменная часть длиннее 255 символов
            long_domain,
            # Очень длинный адрес
            "s" * 100 + "@" + "s" * 150 + ".ru",
            # Имя пользователя начинается с точки
            ".s1@mail.ru",
            # Слишком короткий домен верхнего уровня
            "m1@mail.c",
            # Последовательность подчеркиваний
            "______@mail.ru",
            # Несуществующий домен
            "sofya@outlook.com",
            # Несуществующий домен
            "user@yandex.ru"
        ]
        # Перебираются email-адреса из списка
        for email in list_mail_uncor:
            # Проверяется, что функция is_valid_email возвращает False
            self.assertFalse(
                myform_mail.is_valid_email(email),
                f"Was expected that {email} must be an invalid email"
                )

# Проверяется, запускается ли скрипт напрямую
if __name__ == '__main__':
    # Запускаются все тесты
    unittest.main()
