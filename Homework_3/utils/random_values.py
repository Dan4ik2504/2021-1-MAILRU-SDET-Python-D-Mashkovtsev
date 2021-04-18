import os
import random
import string
import time

DEFAULT_LENGTH = 10


class _RandomValues:
    random_obj = random.Random()

    def init_random_seed(self, config):
        """
        Creates a random seed in the main process and shares it between worker processes
        to avoid the error "Different tests were collected..."
        """
        if config.is_master_process:
            seed = time.time()
            os.environ["mytarget_tests_random_seed"] = str(seed)
        else:
            seed = float(os.environ.get("mytarget_tests_random_seed"))
        self.random_obj.seed(seed)

    # Base methods

    def get_random_letters_and_digits(self, length=DEFAULT_LENGTH):
        return ''.join(self.random_obj.choices(string.ascii_letters + string.digits, k=length))

    def get_random_letters(self, length=DEFAULT_LENGTH):
        return ''.join(self.random_obj.choices(string.ascii_letters, k=length))

    def get_random_digits(self, length=DEFAULT_LENGTH):
        return ''.join(self.random_obj.choices(string.digits, k=length))

    def get_random_bool(self):
        return self.random_obj.choice([True, False])

    # Custom methods

    @property
    def email(self):
        return ''.join((self.get_random_letters_and_digits(10), "@", self.get_random_letters(10), ".com"))

    @property
    def phone_number(self):
        return ''.join(("+7", self.get_random_digits(length=10)))

    @property
    def incorrect_login(self):
        return self.get_random_letters(15)

    @property
    def password(self):
        return self.get_random_letters_and_digits(16)


random_values = _RandomValues()
