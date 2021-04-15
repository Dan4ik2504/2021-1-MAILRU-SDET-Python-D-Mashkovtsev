from dataclasses import dataclass
import faker

from utils import random_values

fake = faker.Faker()


@dataclass
class SegmentData:
    name: str


@dataclass
class CampaignData:
    url: str
    name: str


@dataclass
class CampaignBannerData:
    name: str
    title: str
    text: str
    about_company: str


@dataclass
class UserData:
    email: str
    password: str


class Builder:

    @staticmethod
    def create_segment_data():
        name = fake.text(20)[:-1]
        return SegmentData(name=name)

    @staticmethod
    def create_campaign_banner_data():
        name = fake.text(40)[:-1]
        title = fake.text(20)[:-1]
        text = fake.text(80)
        about_company = fake.text(100)
        return CampaignBannerData(name=name, title=title, text=text, about_company=about_company)

    @staticmethod
    def create_campaign_data():
        url = random_values.get_random_letters_and_digits(random_values.random.randint(10, 30)) + ".com"
        name = fake.text(80)[:-1]
        return CampaignData(url=url, name=name)

    @staticmethod
    def create_user_data():
        email = fake.email()
        password = fake.password(16)
        return UserData(email=email, password=password)
