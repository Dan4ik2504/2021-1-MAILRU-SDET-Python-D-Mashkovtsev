from dataclasses import dataclass
import faker

fake = faker.Faker()


@dataclass
class User:
    first_name: str
    last_name: str


class Builder:

    @staticmethod
    def create_user(first_name=None, last_name=None):
        first_name = first_name or fake.first_name()
        last_name = last_name or fake.last_name()
        return {'first_name': first_name, 'last_name': last_name}

    def create_user_object(self, first_name=None, last_name=None):
        user = self.create_user(first_name, last_name)
        return User(**user)

    def get_users_list_of_tuples(self, count=10):
        users = []
        for _ in range(count):
            user = self.create_user()
            users.append((user['first_name'], user['last_name']))
        return users

    @staticmethod
    def get_different_last_names(count=2):
        last_names = []
        while len(last_names) < count:
            last_name = fake.last_name()
            if last_name not in last_names:
                last_names.append(last_name)
        return last_names