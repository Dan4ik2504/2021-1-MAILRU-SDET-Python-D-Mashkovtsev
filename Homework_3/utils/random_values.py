import random
import string

DEFAULT_LENGTH = 10


# Base methods

def get_random_letters_and_digits(length=DEFAULT_LENGTH):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def get_random_letters(length=DEFAULT_LENGTH):
    return ''.join(random.choices(string.ascii_letters, k=length))


def get_random_digits(length=DEFAULT_LENGTH):
    return ''.join(random.choices(string.digits, k=length))


def get_random_bool():
    return random.choice([True, False])


# Custom methods

def email():
    return ''.join((get_random_letters_and_digits(10), "@", get_random_letters(10), ".com"))


def phone_number():
    return ''.join(("+7", get_random_digits(length=10)))


def incorrect_login():
    return get_random_letters(15)


def password():
    return get_random_letters_and_digits(16)
