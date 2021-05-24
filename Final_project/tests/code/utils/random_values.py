import os
import sys
import time
from faker import Faker


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
        generator_name = f'_{func.__name__}_generator'

        if generator := getattr(self, generator_name, None):
            return next(generator)

        else:
            generator = fake_generator(func, self.seed, self.pid, self.processes_number, self=self, **kwargs)
            setattr(self, generator_name, generator)
            return next(generator)

    return wrapper


class _RandomValues:
    pid = 0
    processes_number = 1

    seed = time.time()

    def __init__(self):
        self.fake = Faker()

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

    @property
    def username(self):
        return self.fake.unique.user_name()

    @property
    def email(self):
        return self.fake.unique.email()

    @property
    def password(self):
        return self.fake.unique.password(16)

    @property
    def id(self):
        return self.fake.unique.random_number()

    @property
    def boolean(self):
        return self.fake.unique.boolean()


class _RandomDifferentValues(_RandomValues):
    """
    Generates the different values between processes when running tests in parallel
    """

    @property
    @separate_fakes_between_processes
    def username(self, fake):
        return fake.unique.user_name()

    @property
    @separate_fakes_between_processes
    def email(self, fake):
        return fake.unique.email()

    @property
    @separate_fakes_between_processes
    def password(self, fake):
        return fake.unique.password(16)

    @property
    @separate_fakes_between_processes
    def id(self, fake):
        return fake.unique.random_number()

    @property
    @separate_fakes_between_processes
    def boolean(self, fake):
        return fake.unique.boolean()


random_equal_values = _RandomEqualValues()
random_different_values = _RandomDifferentValues()
