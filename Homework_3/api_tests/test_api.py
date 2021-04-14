import allure
import pytest

import settings
from api_tests.base import ApiBase


class TestLogin(ApiBase):
    authorize = False

    def get_dashboard(self):
        response = self.api_client.get_request(settings.Url.DASHBOARD, jsonify=False)
        assert response.status_code == 200
        return response

    def verify_login(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.DASHBOARD

    def verify_logout(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.BASE

    @allure.title("Positive login test")
    @pytest.mark.API
    def test_positive_login(self):
        self.login_api.post_login()
        self.verify_login()

    @allure.title("Negative login test")
    @pytest.mark.API
    def test_negative_login(self):
        with pytest.raises(self.login_api.Exceptions.InvalidLogin):
            self.login_api.post_login("1q2w3e", "1q2w3e")
        self.verify_logout()

    @allure.title("Logout test")
    @pytest.mark.API
    def test_logout(self):
        self.login_api.post_login()
        self.verify_login()
        self.login_api.logout()
        self.verify_logout()


class TestCampaigns(ApiBase):
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
    
    def create_campaign(self, repo_root):
        new_camp = self.campaigns_api.get_new_campaign_object()

        new_camp.url = "qwerweqfqwefweqwef.com"
        new_camp.name = "Test name"
        new_camp.objective = new_camp.OBJECTIVES.TRAFFIC
        new_camp.enable_offline_goals = False
        new_camp.set_age(20, 50)
        new_camp.budget_limit_day = 12345
        new_camp.budget_limit = 123456700
        new_camp.targetings.sex_female = True

        interests = new_camp.targetings.interests
        interests.games__computer_games = True
        interests.movies__anime = True

        interests_soc_dem = new_camp.targetings.interests_soc_dem
        interests_soc_dem.income__middle = True
        interests_soc_dem.employment__works = True

        new_banner = new_camp.get_new_banner()
        new_banner.name = "Banner name"
        new_banner.title = "Banner title"
        new_banner.text = "Banner text"
        new_banner.about_company = "Banner about company text"

        images = self.load_images(repo_root)

        new_banner.image_id = images[settings.TestFiles.IMAGE_NAME]
        new_banner.large_image_id = images[settings.TestFiles.LARGE_IMAGE_NAME]
        new_banner.icon_id = images[settings.TestFiles.ICON_NAME]

        new_camp.save_banner(new_banner)

        self.campaigns_api.save_new_campaign(new_camp)

    @allure.title("Create campaign test")
    @pytest.mark.API
    def test_create_campaign(self, repo_root):
        self.create_campaign(repo_root)
