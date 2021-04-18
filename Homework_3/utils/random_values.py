import os
import random
import string
import time

DEFAULT_LENGTH = 10


def init_random_seed(config):
    """
    Creates a random seed in the main process and shares it between worker processes
    to avoid the error "Different tests were collected..."
    """
    if config.is_master_process:
        seed = time.time()
        os.environ["mytarget_tests_random_seed"] = str(seed)
    else:
        seed = float(os.environ.get("mytarget_tests_random_seed"))
    random.seed(seed)


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
