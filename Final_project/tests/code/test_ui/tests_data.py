class LoginPage:
    class ErrorMsgs:
        INVALID_DATA = "Invalid username or password"
        INCORRECT_USERNAME_LENGTH = "Incorrect username length"
        USERNAME_NOT_SPECIFIED = "Необходимо указать логин для авторизации"
        PASSWORD_NOT_SPECIFIED = "Необходимо указать пароль для авторизации"
        NOT_AUTHORIZED = "This page is available only to authorized users"


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
