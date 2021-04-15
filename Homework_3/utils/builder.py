import datetime
from dataclasses import dataclass
import faker
import random

from api.campaigns import NewCampaign
from utils import random_values

fake = faker.Faker()


@dataclass
class SegmentData:
    name: str


@dataclass
class CampaignData:
    url: str
    name: str
    age: list
    budget_limit_day: int
    budget_limit: int
    sex_female: bool
    sex_male: bool
    interests: dict
    interests_soc_dem: dict
    price: str
    date_start: datetime.date
    date_end: datetime.date


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
        url = random_values.get_random_letters_and_digits(random.randint(10, 30)) + ".com"
        name = fake.text(80)[:-1]
        age_fr = random.randint(12, 50)
        age_to = random.randint(age_fr + 5, 76)
        age = list(range(age_fr, age_to))
        budget_limit_day = random.randint(100, 100000000)
        budget_limit = random.randint(100, 100000000) * 100
        price = str(random.randint(1, 50000) / 100)
        date_start = datetime.date.today() + datetime.timedelta(days=random.randint(0, 60))
        date_end = date_start + datetime.timedelta(days=random.randint(20, 90))

        sex = {
            "female": random_values.get_random_bool(),
            "male": random_values.get_random_bool()
        }
        if not any(sex.values()):
            sex[random.choice(["female", "male"])] = True

        interests = {}
        for interest_name in NewCampaign._Targetings._Interests.INTEREST_ID.keys():
            interests[interest_name] = random_values.get_random_bool()

        interests_soc_dem = {}
        for interest_name in NewCampaign._Targetings._InterestsSocDem.INTEREST_ID.keys():
            interests_soc_dem[interest_name] = random_values.get_random_bool()

        return CampaignData(url=url, name=name, age=age, budget_limit_day=budget_limit_day, budget_limit=budget_limit,
                            sex_female=sex['female'], sex_male=sex['male'], interests=interests, price=price,
                            interests_soc_dem=interests_soc_dem, date_start=date_start, date_end=date_end)

    @staticmethod
    def create_user_data():
        email = fake.email()
        password = fake.password(16)
        return UserData(email=email, password=password)
