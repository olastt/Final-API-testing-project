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

    def _load_env(self):
        """Загружает переменные окружения из .env файла"""
        if os.path.exists(".env"):
            load_dotenv(".env", override=True)
            self.api_url = os.getenv("API_URL", "").rstrip("/")
            self.api_name = os.getenv("API_NAME")
            self.token = os.getenv("TOKEN")

    def _validate_environment(self):
        """Проверяет обязательные переменные окружения"""
        if not all([self.api_url, self.api_name]):
            raise ValueError("API_URL и API_NAME должны быть заданы в .env")

    def create_token(self, headers=None):
        """Создает и возвращает токен авторизации"""
        data = {"name": self.api_name}
        headers = headers or {"Content-Type": "application/json"}

        with allure.step(f"Отправка запроса POST {self.api_url}/authorize"):
            self.send_request(method="POST", endpoint="/authorize", data=data, headers=headers)
            self.log_response()
            self.token = self._extract_token_from_response()

        self._update_env_token()

        return self.token

    def _extract_token_from_response(self):
        """Извлекает токен из ответа сервера"""
        try:
            token = self.response.json().get("token")
        except ValueError:
            raise ValueError("Ответ не является JSON и не содержит токен")
        if not token:
            raise ValueError("Токен не найден в теле ответа")
        return token

    def _update_env_token(self):
        """Обновляет токен в .env файле"""
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

    def authorize(self, token_type):
        """Выполняет авторизацию с указанным типом токена"""
        with allure.step("Авторизация с токеном"):
            token = self.get_token_by_type(token_type)
            endpoint = self.build_authorize_endpoint(token)
            self.send_request(method="GET", endpoint=endpoint)
            self.log_response()

    def get_token_by_type(self, token_type):
        """Возвращает токен по указанному типу"""
        return {
            "valid": self.token,
            "none": None,
            "empty": "",
            "invalid": self.generate_invalid_token()
        }.get(token_type, None)

    with allure.step("Формирование endpoint для авторизации"):
        def build_authorize_endpoint(self, token):
            """Формирует endpoint для авторизации"""
            return f"/authorize/{token}" if token else "/authorize/"

    @allure.step("Проверка статуса ответа")
    def verify_expected_status(self, expected_status):
        """Проверяет соответствие статуса ответа ожидаемому"""
        assert self.response.status_code == expected_status, \
            f"Ожидался статус {expected_status}, получен {self.response.status_code}"

    @allure.step("Проверка текста в теле ответа")
    def assert_text_in_response(self):
        """Проверяет наличие токена в теле ответа"""
        if self.response.status_code == 200:
            actual_text = self.response.text.strip()
            expected_text = "Token is alive. Username is"
            assert expected_text in actual_text, (
                f"Ожидалось, что в ответе будет: '{expected_text}', "
                f"но получено: '{actual_text}'"
            )
        else:
            print(f"Пропущена проверка текста: статус-код {self.response.status_code}")
        self.log_response()

    @allure.step("Генерация невалидного токена")
    def generate_invalid_token(self):
        """Генерирует случайный невалидный токен"""
        return secrets.token_hex(16)
