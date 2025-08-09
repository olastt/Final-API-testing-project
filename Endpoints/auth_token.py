from dotenv import load_dotenv
from .base_endpoint import Endpoint
import allure
import secrets
import os


@allure.epic("Авторизация")
class AuthToken(Endpoint):
    def __init__(self):
        super().__init__()
        self._load_env()
        self._validate_environment()
        self.token = None

    @allure.step("Загрузка переменных окружения из .env файла")
    def _load_env(self):
        if os.path.exists(".env"):
            load_dotenv(".env", override=True)
            with allure.step("Чтение переменных API_URL, API_NAME и TOKEN"):
                self.api_url = os.getenv("API_URL", "").rstrip("/")
                self.api_name = os.getenv("API_NAME")
                self.token = os.getenv("TOKEN")

    @allure.step("Проверка обязательных переменных окружения")
    def _validate_environment(self):
        if not all([self.api_url, self.api_name]):
            raise ValueError("API_URL и API_NAME должны быть заданы в .env")

    @allure.step("Создание токена через POST /authorize")
    def create_token(self, headers=None):
        data = {"name": self.api_name}
        headers = headers or {"Content-Type": "application/json"}

        with allure.step("Отправка запроса"):
            self.send_request(method="POST", endpoint="/authorize", data=data, headers=headers)
            self.log_response()

        self.token = self._extract_token_from_response()
        self._update_env_token()
        return self.token

    @allure.step("Извлечение токена из ответа сервера")
    def _extract_token_from_response(self):
        try:
            token = self.response.json().get("token")
        except ValueError:
            raise ValueError("Ответ не является JSON и не содержит токен")

        if not token:
            raise ValueError("Токен не найден в теле ответа")

        return token

    @allure.step("Обновление токена в .env файле")
    def _update_env_token(self):
        if not os.path.exists(".env"):
            return

        with open(".env", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            token_updated = False

            for line in lines:
                if line.startswith("TOKEN="):
                    file.write(f"TOKEN={self.token}\n")
                    token_updated = True
                else:
                    file.write(line)

            if not token_updated:
                file.write(f"TOKEN={self.token}\n")
            file.truncate()

    @allure.step("Авторизация с валидным токеном")
    def authorize_valid_token(self, token):
        endpoint = self.build_authorize_endpoint(token)
        self.send_request(method="GET", endpoint=endpoint)
        self.log_response()

    @allure.step("Авторизация с невалидным токеном")
    def authorize_invalid_token(self):
        invalid_token = self.generate_invalid_token()
        endpoint = self.build_authorize_endpoint(invalid_token)
        self.send_request(method="GET", endpoint=endpoint)
        self.log_response()

    @allure.step("Авторизация без токена")
    def authorize_empty_token(self):
        endpoint = self.build_authorize_endpoint(None)
        self.send_request(method="GET", endpoint=endpoint, token=None)
        self.log_response()

    @allure.step("Формирование endpoint для авторизации")
    def build_authorize_endpoint(self, token):
        return f"/authorize/{token}" if token else "/authorize/"

    @allure.step("Проверка статуса ответа")
    def verify_expected_status(self, expected_status):
        assert self.response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, получен {self.response.status_code}"

    @allure.step("Проверка текста в теле ответа")
    def assert_text_in_response(self, expected_text: str):
        actual_text = self.response.text.strip()
        assert expected_text in actual_text, (
            f"Ожидалось, что в ответе будет: '{expected_text}', "
            f"но получено: '{actual_text}'"
        )
        self.log_response()

    @allure.step("Проверка наличия полей в теле ответа")
    def check_response_in_body(self):
        response_data = self.response.json()
        with allure.step("Проверка наличия поля 'token'"):
            assert "token" in response_data, "Отсутствует поле token"
        with allure.step("Проверка наличия поля 'user'"):
            assert "user" in response_data, "Отсутствует поле user"

    @allure.step("Проверка формата token в теле ответа")
    def check_token_is_string(self):
        token = self.response.json().get("token")
        assert isinstance(token, str), f"Ожидалась строка, но было получено: {type(token)}"
        assert len(token) > 0, f"Токен пустой"

    @allure.step("Проверка поля 'user' в теле ответа")
    def assert_response_match_payload(self):
        expected_user = self.api_name
        response_data = self.response.json()
        actual_name = response_data.get("user")
        assert actual_name == expected_user, (
            f"Ожидалось имя {expected_user}, но было получено {actual_name}"
        )

    @allure.step("Генерация невалидного токена")
    def generate_invalid_token(self):
        return secrets.token_hex(16)

    @allure.step("Проверка html текста при невалидном токене")
    def assert_html_error_response_with_invalid_token(self):
        response_text = self.response.text
        assert "<p>Token not found</p>" in response_text, "Текст ошибки не соответствует"

    @allure.step("Проверка html текста при отсутствии токена")
    def assert_html_error_response_with_empty_token(self):
        response_text = self.response.text
        assert "The requested URL was not found on the server." in response_text, "Текст ошибки не соответствует"
