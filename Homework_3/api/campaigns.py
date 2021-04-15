import datetime
import os

import allure

import settings
from api.client import ApiClient


class NewCampaign:
    url: str = None
    name: str = None
    objective: str = None
    enable_offline_goals: bool = False
    age: list = list(range(12, 76))
    _date_template = "%Y-%m-%d"
    date_start: datetime.date = datetime.date.today()
    date_end: datetime.date = datetime.date.today() + datetime.timedelta(days=30)
    budget_limit_day: int = None
    budget_limit: int = None

    class OBJECTIVES:
        TRAFFIC = 'traffic'

    class _Targetings:
        sex_female = False
        sex_male = False

        def __init__(self):
            self.interests_soc_dem = self._InterestsSocDem()
            self.interests = self._Interests()

        class _InterestsSocDem:

            INTEREST_ID = {
                "employment__not_works": 10245,
                "employment__works": 10244,
                "income__lower_middle": 8674,
                "income__middle": 8675,
                "income__upper_middle": 8676,
                "income__high": 8677,
                "income__premium": 8678
            }

            employment__not_works = False
            employment__works = False
            income__lower_middle = False
            income__middle = False
            income__upper_middle = False
            income__high = False
            income__premium = False

            def get_list(self):
                interests = []
                for interest_name, interest_id in self.INTEREST_ID.items():
                    if self.__getattribute__(interest_name) is True:
                        interests.append(interest_id)
                return interests

        class _Interests:

            INTEREST_ID = {
                "games__browser_games": 8797,
                "games__streams": 21580,
                "games__computer_games": 14393,
                "movies__anime": 11827
            }

            games__browser_games = False
            games__streams = False
            games__computer_games = False
            movies__anime = False

            def get_list(self):
                interests = []
                for interest_name, interest_id in self.INTEREST_ID.items():
                    if self.__getattribute__(interest_name) is True:
                        interests.append(interest_id)
                return interests

    class NewBanner:
        name: str = None
        title: str = None
        text: str = None
        about_company: str = None
        image_id: int = None
        large_image_id: int = None
        icon_id: int = None

        def __init__(self, url_id: int):
            self.url_id = url_id

        def get_json(self):
            json = {
                'urls': {'primary': {'id': self.url_id}},
                'textblocks': {
                    'title_25': {'text': self.title},
                    'text_90': {'text': self.text},
                    'about_company_115': {'text': self.about_company},
                    'cta_sites_full': {'text': 'visitSite'}},
                'content': {'image_600x600': {'id': self.image_id},
                            'image_1080x607': {'id': self.large_image_id},
                            'icon_256x256': {'id': self.icon_id}},
                'name': self.name
            }

            return json

    def __init__(self, campaigns_api):
        self.campaigns_api = campaigns_api
        self.targetings = self._Targetings()
        self._banners_list = []

    @allure.step("Getting ID of the campaign URL")
    def get_url_id(self):
        """Sends a request and returns ID of the campaign URL"""
        self.campaigns_api.logger.info(f'Getting ID of the campaign URL: "{self.url}"')
        params = {"url": self.url}
        response = self.campaigns_api.get_request(settings.Url.Api.CAMPAIGNS_REGISTER_URL_GET, params=params)
        return response['id']

    def get_new_banner(self):
        """Creates a new banner instance"""
        return self.NewBanner(self.get_url_id())

    def save_banner(self, banner):
        """Adds a new banner to the banners list"""
        self._banners_list.append(banner)

    def generate_json(self):
        """Creates data for a request in the form of a dictionary, which is serializable in JSON"""
        sex = []
        if self.targetings.sex_male:
            sex.append('male')

        if self.targetings.sex_female:
            sex.append('female')

        banners = []
        for banner in self._banners_list:
            banners.append(banner.get_json())

        json = {
            'name': self.name,
            'conversion_funnel_id': None,
            'objective': self.objective,
            'enable_offline_goals': self.enable_offline_goals,
            'targetings': {
                'split_audience': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'sex': sex,
                'age': {
                    'age_list': self.age,
                    'expand': False},
                'geo': {'regions': [188]},
                'interests_soc_dem': self.targetings.interests_soc_dem.get_list(),
                'segments': [],
                'interests': self.targetings.interests.get_list(),
                'fulltime': {
                    'flags': ['use_holidays_moving', 'cross_timezone'],
                    'mon': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'tue': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'wed': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'thu': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'fri': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'sat': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23],
                    'sun': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                            18, 19, 20, 21, 23]
                },
                'pads': [102634, 102643],
                'mobile_types': ['tablets', 'smartphones'],
                'mobile_vendors': [],
                'mobile_operators': []
            },
            'age_restrictions': None,
            'date_start': self.date_start.strftime(self._date_template),
            'date_end': self.date_end.strftime(self._date_template),
            'autobidding_mode': 'second_price_mean',
            'budget_limit_day': self.budget_limit_day,
            'budget_limit': self.budget_limit,
            'mixing': 'recommended',
            'utm': None,
            'enable_utm': True,
            'price': '7.38',
            'max_price': '0',
            'package_id': 811,
            'banners': banners
        }

        return json

    def set_age(self, fr: int, to: int):
        """Setting age.
        Min: 12. Max: 75"""
        self.age = list(range(fr, to))

    @allure.step("New campaign saving")
    def save(self):
        """Sends a request to save a new campaign"""
        self.campaigns_api.logger.info(f'New campaign "{self.name}" saving')
        request_data = self.generate_json()
        self.campaigns_api.post_request(settings.Url.Api.CAMPAIGNS, json=request_data)
        self.campaigns_api.logger.info(f'Campaign "{self.name}" saved')


class Campaign:
    def __init__(self, data_dict, campaigns_api):
        self.campaigns_api = campaigns_api
        self.id = data_dict["id"]
        self.name = data_dict["name"]

    @allure.step("Campaign deletion")
    def delete(self):
        """Sends a request to delete a campaign"""
        data = [{
            "id": self.id,
            "status": "deleted"
        }]
        self.campaigns_api.post_request(settings.Url.Api.CAMPAIGNS_MASS_ACTION, json=data, expected_status=204,
                                        jsonify=False)
        self.campaigns_api.logger.info(f'Campaign "{str(self)}" deleted')

    def __eq__(self, other):
        if other.isdigit() or isinstance(other, int):
            return self.id == int(other)
        else:
            return self.name == str(other)

    def __repr__(self):
        return f'{self.id}-{self.name}'


class CampaignsApi(ApiClient):

    class Exceptions(ApiClient.Exceptions):
        class CampaignNotExists(Exception):
            pass

    @allure.step('Image "{img_name}" uploading')
    def load_image(self, img_name, repo_root, test_files_dir=settings.Basic.TEST_FILES_DIR):
        """Uploads an image to the server and returns the image ID"""
        upload_url = settings.Url.Api.STATIC_POST
        image_path = os.path.join(repo_root, test_files_dir, img_name)

        self.logger.info(f'Image "{img_name}" uploading to the "{upload_url}"')
        self.logger.debug(f'Image path: "{image_path}"')

        with open(image_path, "rb") as file:
            files = {'file': file}
            response = self.post_request(url=upload_url, files=files)
            return response["id"]

    @allure.step("Searching for active campaigns")
    def get_active_campaigns(self):
        """Returns active campaigns"""
        self.logger.info("Searching for active campaigns")
        params = {
            "fields": ','.join(['id', 'name']),
            "sorting": "-id",
            "_status__in": "active",
        }
        campaigns_dicts = self.get_request(settings.Url.Api.CAMPAIGNS, params=params)['items']
        campaigns_objects = []
        for campaign_dict in campaigns_dicts:
            campaign_object = Campaign(campaign_dict, self)
            campaigns_objects.append(campaign_object)

        self.logger.info(f'{len(campaigns_objects)} active campaigns exists. {len(campaigns_dicts)} campaigns in total')
        self.logger.debug(f'There are {len(campaigns_objects)} active campaigns: '
                          f'"{"; ".join([str(c) for c in campaigns_objects])}"')
        return campaigns_objects

    def get_new_campaign_object(self):
        """Returns new campaign instance"""
        return NewCampaign(self)

    def get_campaign_by_name(self, campaign_name):
        """Returns campaign found by the given name"""
        campaigns = self.get_active_campaigns()
        for campaign in campaigns:
            if campaign.name == campaign_name:
                return campaign
        raise self.Exceptions.CampaignNotExists(f'Campaign with name "{campaign_name}" does not exists')
