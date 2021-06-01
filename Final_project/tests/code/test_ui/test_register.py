import pytest
from selenium.webdriver.common.keys import Keys
from itertools import product

from test_ui.base import BaseUICase
import tests_data
from utils.random_values import random_equal_values as rand_val_eq


class TestRegisterPage(BaseUICase):
    authorize = False
    form_errors = tests_data.RegisterPage.ErrorMsgs

    @pytest.fixture(scope='function', autouse=True)
    def open_register_page(self, setup):
        self.register_page.open_page()

    # Methods

    def do_register_existing_user(self, username, email, password):
        self.register_page.register(username=username, password=password, email=email)
        self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.USER_EXISTS

    # Tests

    def test_go_to_login_page(self):
        """
        Тест перехода на страницу авторизации через ссылку внизу формы

        Шаги:
        1. Клик на ссылку

        ОР: Открылась страница авторизации
        """

        self.register_page.click(self.register_page.locators.LOGIN_PAGE_LINK)
        self.login_page.wait_until.is_page_opened()
        assert self.login_page.check.is_page_url_match_driver_url()

    def test_register_form__positive(self):
        """
        Позитивный тест регистрации

        Шаги:
        1. Отправка формы с валидными именем, паролем и почтой

        ОР: Открылась главная страница. Данные нового пользователя внесены в БД
        """

        user = self.users_builder.generate_user(save_in_db=False)
        self.register_page.register(username=user.username, password=user.password, email=user.email)
        self.main_page.wait_until.is_page_opened()
        assert self.myapp_db.is_user_exists(username=user.username, password=user.password, email=user.email)

    def test_register_form__existing_user(self):
        """
        Негативный тест регистрации существующего пользователя

        Шаги:
        1. Создание нового пользователя
        2. Отправка формы с данными нового пользователя

        ОР: Отобразилось сообщение об ошибке "Пользователь существует"
        """

        user = self.users_builder.generate_user()
        self.do_register_existing_user(username=user.username, password=user.password, email=user.email)

    def test_register_form__existing_username(self):
        """
        Негативный тест регистрации пользователя c существующим в БД именем

        Шаги:
        1. Создание нового пользователя
        2. Отправка формы с именем нового пользователя

        ОР: Отобразилось сообщение об ошибке "Пользователь существует"
        """

        user = self.users_builder.generate_user()
        password = self.fake.get_password()
        email = self.fake.get_email()
        self.do_register_existing_user(username=user.username, password=password, email=email)
        assert not self.myapp_db.is_user_exists(password=password, email=email)

    def test_register_form__existing_email(self):
        """
        Негативный тест регистрации пользователя c существующим в БД email

        Шаги:
        1. Создание нового пользователя
        2. Отправка формы с email нового пользователя

        ОР: Отобразилось сообщение об ошибке "Пользователь существует"
        """

        user = self.users_builder.generate_user()
        username = self.fake.get_username()
        password = self.fake.get_password()
        self.do_register_existing_user(username=username, password=password, email=user.email)
        assert not self.myapp_db.is_user_exists(username=username, password=password)

    def test_register_form__existing_password(self):
        """
        Тест регистрации пользователя c существующим в БД паролем

        Шаги:
        1. Создание нового пользователя
        2. Отправка формы с паролем нового пользователя

        ОР: Открылась главная страница. Пользователь создан
        """

        user = self.users_builder.generate_user()
        username = self.fake.get_username()
        email = self.fake.get_email()
        self.register_page.register(username=username, password=user.password, email=email)
        self.main_page.wait_until.is_page_opened()
        assert self.myapp_db.is_user_exists(username=username, email=email)

    @pytest.mark.parametrize(
        'email',
        (
            '{}@{}.{}'.format(*i) for i in list(filter(
                lambda l: '' in l and any(l),
                product(
                    ('', rand_val_eq.get_random_letters_and_digits(6)),
                    ('', rand_val_eq.get_random_letters_and_digits(6)),
                    ('', rand_val_eq.get_random_letters_and_digits(6))
                )
            ))
        )
    )
    def test_register_form__incorrect_email(self, email):
        """
        Негативный тест регистрации пользователя c некорректным email

        Шаги:
        1. Отправка формы с некорректным email

        ОР: Пользователь не создан. Отображается сообщение об ошибке "Некорректный email"
        """

        username = self.fake.get_username()
        password = self.fake.get_password()

        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, password=password, email=email)
            self.register_page.wait_until.is_page_opened()

        assert self.register_page.get_error_text() == self.form_errors.INVALID_EMAIL
        assert not self.myapp_db.is_user_exists(username=username, email=email, password=password)

    def test_register_form__do_not_repeat_password_1(self):
        """
        Негативный тест отправки формы регистрации с незаполненным полем "Repeat password", но заполненным "Password"

        Шаги:
        1. Отправка формы с заполненным полем "Password", но пустым полем "Repeat password"

        ОР: Страница не перезагрузилась (т.е. POST запрос не отправился). Пользователь не создан
        """

        user = self.users_builder.generate_user(save_in_db=False)

        with self.register_page.is_page_not_reloaded__context_manager():
            self.register_page.register(user.username, user.email, user.password, '')
            self.register_page.wait_until.is_page_opened()

        assert self.register_page.check.is_not_visible(self.register_page.locators.ERROR_TEXT)

    def test_register_form__do_not_repeat_password_2(self):
        """
        Негативный тест отправки формы регистрации с незаполненным полем "Password", но заполненным "Repeat password"

        Шаги:
        1. Отправка формы с заполненным полем "Repeat password", но пустым полем "Password"

        ОР: Страница не перезагрузилась (т.е. POST запрос не отправился). Пользователь не создан
        """

        user = self.users_builder.generate_user(save_in_db=False)

        with self.register_page.is_page_not_reloaded__context_manager():
            self.register_page.register(user.username, user.email, '', user.password)
            self.register_page.wait_until.is_page_opened()

        assert self.register_page.check.is_not_visible(self.register_page.locators.ERROR_TEXT)

    def test_register_form__passwords_not_match(self):
        """
        Негативный тест отправки формы регистрации с различающимися паролями в полях "Password" и "Repeat password"

        Шаги:
        1. Отправка формы с разными паролями в полях "Password" и "Repeat password"

        ОР: Отобразилось сообщение об ошибке "Пароли должны совпадать". Пользователь не создан
        """

        user = self.users_builder.generate_user(save_in_db=False)

        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(user.username, user.email, self.fake.get_password(), self.fake.get_password())
            self.register_page.wait_until.is_page_opened()

        assert self.register_page.get_error_text() == self.form_errors.PASSWORDS_MUST_MATCH

    @pytest.mark.parametrize(
        ('username', 'email', 'password'),
        (
                list(
                    filter(
                        lambda l: '' in l,
                        product(('', rand_val_eq.get_username()), ('', rand_val_eq.get_email()), ('', rand_val_eq.get_password())),
                    )
                )
        )
    )
    def test_register_form__empty_data(self, username, email, password):
        """
        Негативный тест отправки формы регистрации с пустыми полями

        Шаги:
        1. Отправка формы с пустыми полями

        ОР: Страница не перезагрузилась (т.е. POST запрос не отправился). Пользователь не создан
        """

        with self.register_page.is_page_not_reloaded__context_manager():
            self.register_page.register(username=username, password=password, email=email)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.check.is_not_visible(self.register_page.locators.ERROR_TEXT)
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    def test_register_form__incorrect_empty_username(self):
        """
        Негативный тест регистрации с именем, состоящим из символа "пробел"

        Шаги:
        1. Отправка формы с именем, состоящим из символа "пробел"

        ОР: Отобразилось сообщение ошибке "Имя пользователя не определено". Пользователь не создан
        """

        username = Keys.SPACE
        email = self.fake.get_email()
        password = self.fake.get_password()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.USERNAME_NOT_SPECIFIED
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    def test_register_form__incorrect_empty_email(self):
        """
        Негативный тест регистрации с email, состоящим из символа "пробел"

        Шаги:
        1. Отправка формы с email, состоящим из символа "пробел"

        ОР: Отобразилось сообщение ошибке "Email не определен". Пользователь не создан
        """

        email = Keys.SPACE
        username = self.fake.get_username()
        password = self.fake.get_password()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.EMAIL_NOT_SPECIFIED
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    def test_register_form__incorrect_empty_password(self):
        """
        Негативный тест регистрации с паролем, состоящим из символа "пробел"

        Шаги:
        1. Отправка формы с паролем, состоящим из символа "пробел"

        ОР: Отобразилось сообщение ошибке "Пароль не определен". Пользователь не создан
        """

        password = Keys.SPACE
        username = self.fake.get_username()
        email = self.fake.get_email()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.PASSWORD_NOT_SPECIFIED
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'username',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
    )
    def test_register_form__incorrect_username_length(self, username):
        """
        Негативный тест регистрации с именем пользователя некорректной длины

        Шаги:
        1. Отправка формы с именем пользователя некорректной длины

        ОР: Отобразилось сообщение ошибке "Некорректная длина имени пользователя". Пользователь не создан
        """

        email = self.fake.get_email()
        password = self.fake.get_password()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.INCORRECT_USERNAME_LENGTH
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'email',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5]]
    )
    def test_register_form__incorrect_email_length(self, email):
        """
        Негативный тест регистрации с email некорректной длины

        Шаги:
        1. Отправка формы с email некорректной длины

        ОР: Отобразилось сообщение ошибке "Некорректная длина email". Пользователь не создан
        """

        username = self.fake.get_username()
        password = self.fake.get_password()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.INCORRECT_EMAIL_LENGTH
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'password',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5]]
    )
    def test_register_form__incorrect_password_length(self, password):
        """
        Негативный тест регистрации с коротким паролем (меньше 6 символов)

        Шаги:
        1. Отправка формы с паролем некорректной длины

        ОР: Отобразилось сообщение ошибке "Некорректная длина пароля". Пользователь не создан
        """

        username = self.fake.get_username()
        email = self.fake.get_email()
        with self.register_page.is_page_reloaded__context_manager():
            self.register_page.register(username=username, email=email, password=password)
            self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == self.form_errors.INCORRECT_PASSWORD_LENGTH
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    def test_register_form__do_not_click_on_sdet_checkbox(self):
        """
        Тест регистрации со снятым чекбоксом "Я согласен с тем, что хочу быть SDET"

        Шаги:
        1. Отправка формы со снятым чекбоксом

        ОР: Страница не перезагрузилась (т.е. POST запрос не отправился). Пользователь не создан
        """

        user = self.users_builder.generate_user(save_in_db=False)

        with self.register_page.is_page_not_reloaded__context_manager():
            self.register_page.register(username=user.username, email=user.email, password=user.password, sdet=False)
            self.register_page.wait_until.is_page_opened()

        assert not self.myapp_db.is_user_exists(username=user.username, password=user.password, email=user.email)

    def test_register_form__more_than_one_errors(self):
        """
        Тест отображения нескольких сообщений об ошибках в форме

        Шаги:
        1. Отправка формы с данными некорректной длины

        ОР: Корректно отобразились ошибки о некорректной длине имени, email и пароля
        """

        username = rand_val_eq.get_random_letters_and_digits(3)
        email = "{}@{}.{}".format(*[rand_val_eq.get_random_letters(1) for _ in range(3)])
        password = rand_val_eq.get_random_letters_and_digits(3)
        self.register_page.register(username=username, email=email, password=password)
        self.register_page.wait_until.is_page_opened()
        assert self.register_page.get_error_text() == f"{self.form_errors.INCORRECT_USERNAME_LENGTH}\n" \
                                                      f"{self.form_errors.INCORRECT_EMAIL_LENGTH}\n" \
                                                      f"{self.form_errors.INCORRECT_PASSWORD_LENGTH}"

        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)
