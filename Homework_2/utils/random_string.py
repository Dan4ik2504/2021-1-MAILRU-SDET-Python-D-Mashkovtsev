import random
import string


def get_random_letters_and_digits(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_random_letters(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))


def get_random_digits(length=10):
    return ''.join(random.choices(string.digits, k=length))


def get_random_email():
    return ''.join((get_random_letters_and_digits(10), "@", get_random_letters(10), ".com"))


def get_random_phone_number():
    return ''.join(("+7", get_random_digits(length=10)))
