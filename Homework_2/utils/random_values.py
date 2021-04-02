import errno
import json
import os
import pathlib
import random
import string
from functools import wraps
from pathlib import Path
import settings

DEFAULT_LENGTH = 10


class Caching:
    FILENAME = "random_values_cache.json"
    ATTRS = (
        'email',
        'phone_number',
        'incorrect_login',
        'password'
    )
    CACHE = {}

    @classmethod
    def caching(cls, func):
        def decorated_func(*args, **kwargs):
            if func.__name__ in cls.CACHE:
                return cls.CACHE[func.__name__]
            result = func(*args, **kwargs)
            cls.CACHE[func.__name__] = result
            return func(*args, **kwargs)

        return decorated_func

    @classmethod
    def get_cache_file_path(cls):
        return os.path.abspath(os.path.join(pathlib.Path(__file__).parent.absolute(),
                                            settings.Basic.TEMPORARY_FILES_DIR, cls.FILENAME))

    @classmethod
    def create_file(cls, path):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    @classmethod
    def create_cache(cls):
        cls.CACHE = {}
        for attr in cls.ATTRS:
            result = getattr(RandomValues, attr)
            cls.CACHE[attr] = result
        cls.write_cache_in_json()

    @classmethod
    def write_cache_in_json(cls):
        cls.create_file(cls.get_cache_file_path())
        with open(cls.get_cache_file_path(), 'w') as f:
            json.dump(cls.CACHE, f)

    @classmethod
    def read_cache_from_json(cls):
        with open(cls.get_cache_file_path(), 'r') as f:
            result = json.load(f)
        if result:
            cls.CACHE = result
        else:
            cls.CACHE = {}


class RandomValues:
    @classmethod
    def get_random_letters_and_digits(self, length=DEFAULT_LENGTH):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @classmethod
    def get_random_letters(self, length=DEFAULT_LENGTH):
        return ''.join(random.choices(string.ascii_letters, k=length))

    @classmethod
    def get_random_digits(self, length=DEFAULT_LENGTH):
        return ''.join(random.choices(string.digits, k=length))

    @classmethod
    @property
    @Caching.caching
    def email(self):
        return ''.join((self.get_random_letters_and_digits(10), "@", self.get_random_letters(10), ".com"))

    @classmethod
    @property
    @Caching.caching
    def phone_number(self):
        return ''.join(("+7", self.get_random_digits(length=10)))

    @classmethod
    @property
    @Caching.caching
    def incorrect_login(self):
        return self.get_random_letters(15)

    @classmethod
    @property
    @Caching.caching
    def password(self):
        return self.get_random_letters_and_digits(16)
