import allure
import pytest

import settings
from base import ApiTestsBase
from utils.builder import Builder
import exceptions
from utils.random_values import random_values


class TestLogin(ApiTestsBase):
    authorize = False

    @allure.step("GET request to the dashboard page")
    def get_dashboard(self):
        response = self.api_client.get_request(settings.Url.DASHBOARD, jsonify=False)
        assert response.status_code == 200
        return response

    @allure.step("Checking that login is success")
    def verify_login(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.DASHBOARD

    @allure.step("Checking that logout is success")
    def verify_logout(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.BASE

    @allure.title("Positive login test")
    @pytest.mark.API
    def test_positive_login(self):
        self.login_api.login()
        self.verify_login()

    @pytest.mark.parametrize(
        ("login", "password"),
        (
                (random_values.email, random_values.password),
                (random_values.phone_number, random_values.password),
                (random_values.email, settings.User.PASSWORD),
                (settings.User.LOGIN, random_values.password),
                (random_values.incorrect_login, random_values.password),
        )
    )
    @allure.title("Negative login test")
    @pytest.mark.API
    def test_negative_login(self, login, password):
        with pytest.raises(exceptions.LoginError):
            self.login_api.login(login, password)
        self.verify_logout()

    @allure.title("Logout test")
    @pytest.mark.API
    def test_logout(self):
        self.login_api.login()
        self.verify_login()
        self.login_api.logout()
        self.verify_logout()


class TestCampaigns(ApiTestsBase):
    @allure.step("Loading banner images")
    def load_images(self, repo_root):
        """Loading banner images"""
        images = ((settings.TestFiles.ICON_FILE, settings.TestFiles.ICON_NAME),
                  (settings.TestFiles.IMAGE_FILE, settings.TestFiles.IMAGE_NAME),
                  (settings.TestFiles.LARGE_IMAGE_FILE, settings.TestFiles.LARGE_IMAGE_NAME))
        images_loaded = {}
        for img_file, img_name in images:
            img_id = self.campaigns_api.load_image(img_file, repo_root=repo_root)
            images_loaded[img_name] = img_id
        return images_loaded

    @allure.step("Campaign creation")
    def create_campaign(self, repo_root):
        new_camp = self.campaigns_api.get_new_campaign_object()
        fake_campaign = Builder.create_campaign_data()

        campaign_name = fake_campaign.name

        new_camp.url = fake_campaign.url
        new_camp.name = campaign_name
        new_camp.objective = new_camp.OBJECTIVES.TRAFFIC
        new_camp.age = fake_campaign.age
        new_camp.budget_limit_day = fake_campaign.budget_limit_day
        new_camp.budget_limit = fake_campaign.budget_limit
        new_camp.targetings.sex_female = fake_campaign.sex_female
        new_camp.targetings.sex_male = fake_campaign.sex_male
        new_camp.price = fake_campaign.price
        new_camp.date_start = fake_campaign.date_start
        new_camp.date_end = fake_campaign.date_end

        interests = new_camp.targetings.interests
        for interest_name, interest_value in fake_campaign.interests.items():
            interests.__setattr__(interest_name, interest_value)

        interests_soc_dem = new_camp.targetings.interests_soc_dem
        for interest_name, interest_value in fake_campaign.interests_soc_dem.items():
            interests_soc_dem.__setattr__(interest_name, interest_value)

        fake_banner = Builder.create_campaign_banner_data()

        new_banner = new_camp.get_new_banner()
        new_banner.name = fake_banner.name
        new_banner.title = fake_banner.title
        new_banner.text = fake_banner.text
        new_banner.about_company = fake_banner.about_company

        images = self.load_images(repo_root)

        new_banner.image_id = images[settings.TestFiles.IMAGE_NAME]
        new_banner.large_image_id = images[settings.TestFiles.LARGE_IMAGE_NAME]
        new_banner.icon_id = images[settings.TestFiles.ICON_NAME]

        new_camp.save_banner(new_banner)

        new_camp.save()

        return campaign_name

    @allure.step("Checking campaign creation")
    def verify_campaign_creation(self, campaign_name):
        campaigns = self.campaigns_api.get_active_campaigns()
        assert campaign_name in campaigns

    @allure.step("Campaign deletion")
    def delete_campaign(self, campaign_name):
        campaign = self.campaigns_api.get_campaign_by_name(campaign_name)
        campaign.delete()

    @allure.step("Checking campaign deletion")
    def verify_campaign_deletion(self, campaign_name):
        campaigns = self.campaigns_api.get_active_campaigns()
        assert campaign_name not in campaigns

    @allure.title("Create campaign test")
    @pytest.mark.API
    def test_create_campaign(self, repo_root):
        campaign_name = self.create_campaign(repo_root)
        self.verify_campaign_creation(campaign_name)
        self.delete_campaign(campaign_name)

    @allure.title("Delete campaign test")
    @pytest.mark.API
    def test_delete_campaign(self, repo_root):
        campaign_name = self.create_campaign(repo_root)
        self.verify_campaign_creation(campaign_name)
        self.delete_campaign(campaign_name)
        self.verify_campaign_deletion(campaign_name)


class TestSegments(ApiTestsBase):
    @allure.step("Segment creation")
    def create_segment(self):
        fake_segment = Builder.create_segment_data()
        segment_name = fake_segment.name
        new_segment = self.segments_api.get_new_segment_object()
        new_segment.name = segment_name
        new_segment.save()
        return segment_name

    @allure.step("Checking segment creation")
    def verify_segment_creation(self, segment_name):
        segments = self.segments_api.get_all_segments()
        assert segment_name in segments

    @allure.step("Segment deletion")
    def delete_segment(self, segment_name):
        segment = self.segments_api.get_segment_by_name(segment_name)
        segment.delete()

    @allure.step("Checking segment deletion")
    def verify_segment_deletion(self, segment_name):
        segments = self.segments_api.get_all_segments()
        assert segment_name not in segments

    @allure.title("Create segment")
    @pytest.mark.API
    def test_create_segment(self):
        segment_name = self.create_segment()
        self.verify_segment_creation(segment_name)
        self.delete_segment(segment_name)

    @allure.title("Delete segment")
    @pytest.mark.API
    def test_delete_segment(self):
        segment_name = self.create_segment()
        self.verify_segment_creation(segment_name)
        self.delete_segment(segment_name)
        self.verify_segment_deletion(segment_name)
