import os
import string
import sys
import time

from faker import Faker

import exceptions
import settings


def fake_generator(func, seed, pid, proc_num, **kwargs):
    fake = Faker()
    fake.seed_instance(seed)
    cur_id = 0
    while True:
        res = func(fake=fake, **kwargs)
        if cur_id == pid:
            yield res
        cur_id += 1
        if cur_id == proc_num:
            cur_id = 0


def separate_fakes_between_processes(func):
    def wrapper(self, **kwargs):
        kwargs_list = []
        for k, v in kwargs.items():
            kwargs_list.append(f"{str(k)}={str(v)}")
        generator_name = f'_{func.__name__}_generator[{";".join(kwargs_list)}]'

        if generator := self._fake_generators.get(generator_name, None):
            return next(generator)

        else:
            generator = fake_generator(func, self.seed, self.pid, self.processes_number, self=self, **kwargs)
            self._fake_generators[generator_name] = generator
            return next(generator)

    return wrapper


def get_value_by_filter_func(func, filter_func, retry=settings.RANDOMIZER.MAX_RETRIES, *args, **kwargs):
    attempt = 0
    while attempt < retry:
        attempt += 1
        value = func(*args, **kwargs)
        if filter_func(value):
            return value
    raise exceptions.TooManyRetries(f"Too many retries to get a random value. Max retries: {retry}")


class _RandomValues:
    pid = 0
    processes_number = 1

    seed = time.time()

    def __init__(self):
        self.fake = Faker()
        self._fake_generators = {}
        self._unique_values = {}

    def init_random_seed(self, config):
        """
        Creates a random seed in the main process and shares it between worker processes
        to avoid the error "Different tests were collected..."
        """
        args = sys.argv
        self.args = args
        if config.is_master_process:
            seed = time.time()
            os.environ["tests_random_seed"] = str(seed)
        else:
            seed = float(os.environ.get("tests_random_seed"))
        self.fake.seed_instance(seed)
        self.seed = seed

        workerinput = getattr(config, 'workerinput', None)
        if workerinput:
            self.pid = int(workerinput['workerid'].lstrip('gw'))
            self.processes_number = int(os.environ.get('PYTEST_XDIST_WORKER_COUNT'))


class _RandomEqualValues(_RandomValues):
    """
    Generates the equal values between processes when running tests in parallel
    """

    _empty_value_current_length = 0

    def get_username(self):
        return get_value_by_filter_func(self.fake.unique.user_name, lambda i: 6 <= len(i) <= 16)

    def get_email(self):
        return self.fake.unique.email()

    def get_password(self):
        return self.fake.unique.password(16)

    def get_id(self):
        return self.fake.unique.random_number()

    def get_boolean(self):
        return self.fake.unique.boolean()

    def get_random_letters_and_digits(self, length=settings.RANDOMIZER.DEFAULT_LENGTH):
        return ''.join(self.fake.random_choices(string.ascii_letters + string.digits, length))

    def get_random_letters(self, length=settings.RANDOMIZER.DEFAULT_LENGTH):
        return ''.join(self.fake.random_choices(string.ascii_letters, length))

    def get_empty_value(self):
        self._empty_value_current_length += 1
        return ' ' * self._empty_value_current_length


class _RandomDifferentValues(_RandomValues):
    """
    Generates the different values between processes when running tests in parallel
    """

    _empty_value_current_length = None

    @separate_fakes_between_processes
    def _get_username(self, fake):
        return get_value_by_filter_func(fake.unique.user_name, lambda i: 6 <= len(i) <= 16)

    def get_username(self):
        return self._get_username()

    @separate_fakes_between_processes
    def _get_email(self, fake):
        return fake.unique.email()

    def get_email(self):
        return self._get_email()

    @separate_fakes_between_processes
    def _get_password(self, fake):
        return fake.unique.password(16)

    def get_password(self):
        return self._get_password()

    @separate_fakes_between_processes
    def _get_id(self, fake):
        return fake.unique.random_number()

    def get_id(self):
        return self._get_id()

    @separate_fakes_between_processes
    def _get_boolean(self, fake):
        return fake.unique.boolean()

    def get_boolean(self):
        return self.get_boolean()

    def get_empty_value(self):
        if self._empty_value_current_length is None:
            self._empty_value_current_length = self.pid + 2
        else:
            self._empty_value_current_length += self.processes_number
        return ' ' * self._empty_value_current_length

    def get_random_string(self, length=settings.RANDOMIZER.DEFAULT_LENGTH):
        answer = ''
        while len(answer) <= length:
            answer += self.get_password()
        return answer[:length]


random_equal_values = _RandomEqualValues()
random_different_values = _RandomDifferentValues()
