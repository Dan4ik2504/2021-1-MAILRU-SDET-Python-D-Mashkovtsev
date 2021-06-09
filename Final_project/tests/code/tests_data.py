import settings


class LoginPage:
    class ErrorMsgs:
        INVALID_DATA = "Invalid username or password"
        INCORRECT_USERNAME_LENGTH = "Incorrect username length"
        USERNAME_NOT_SPECIFIED = "Необходимо указать логин для авторизации"
        PASSWORD_NOT_SPECIFIED = "Необходимо указать пароль для авторизации"
        NOT_AUTHORIZED = "This page is available only to authorized users"
        BLOCKED_USER = "Ваша учетная запись заблокирована"


class RegisterPage:
    class ErrorMsgs:
        USER_EXISTS = "User already exist"
        INCORRECT_USERNAME_LENGTH = "Incorrect username length"
        INCORRECT_EMAIL_LENGTH = "Incorrect email length"
        INCORRECT_PASSWORD_LENGTH = "Incorrect password length"
        USERNAME_NOT_SPECIFIED = "Необходимо указать логин для регистрации"
        EMAIL_NOT_SPECIFIED = "Необходимо указать адрес электронной почты для регистрации"
        PASSWORD_NOT_SPECIFIED = "Необходимо указать пароль для регистрации"
        PASSWORDS_MUST_MATCH = "Passwords must match"
        INVALID_EMAIL = "Invalid email address"


class MainPage:
    USERNAME_TEMPLATE = "Logged as {}"
    VK_ID_TEMPLATE = "VK ID: {}"
    POWERED_BY = "powered by ТЕХНОАТОМ"
    BODY_BUTTONS = (
        {
            'title': "What is an API?",
            'link': settings.EXTERNAL_URLS.WHAT_IS_AN_API
        },
        {
            'title': "Future of internet",
            'link': settings.EXTERNAL_URLS.FUTURE_OF_INTERNET
        },
        {
            'title': "Lets talk about SMTP?",
            'link': settings.EXTERNAL_URLS.SMTP
        }
    )


class Api:
    USER_ADDED = "User was added!"
    CANT_ADD_USER = "Can not add user: "
    CANT_ADD_USER__MISSING_USERNAME = CANT_ADD_USER + "'username'"
    CANT_ADD_USER__MISSING_EMAIL = CANT_ADD_USER + "'email'"
    CANT_ADD_USER__MISSING_PASSWORD = CANT_ADD_USER + "'password'"
    AUTHORIZATION_FAILED = "session lifetime expires"
    STATUS_OK = 'ok'
    USER_BLOCKED = "User was blocked!"
    USER_UNBLOCKED = "User access granted!"
    USER_DOES_NOT_EXIST = "User does not exist!"
