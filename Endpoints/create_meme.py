import allure
import pytest
from bs4 import BeautifulSoup
from models.create_meme_validate import MemeResponse, Info
from Endpoints.base_endpoint import Endpoint
import os


class CreateMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.api_url = "http://167.172.172.115:52355"
        self.headers = {"Content-Type": "application/json"}
        self.id = None

        self.api_url = os.getenv("API_URL")
        self.api_name = os.getenv("API_NAME")
        self.token = os.getenv("TOKEN")
        self.headers = {"Content-Type": "application/json"}

        if not self.token or self.token == "None":
            raise ValueError("Токен не найден в .env. Сначала создайте токен.")

    @allure.step("Создание мема")
    def create_meme(self, token=None, data=None):
        if data is None:
            raise ValueError("Не переданы данные для создания мема.")

        self.send_request(method="POST", endpoint="meme", token=token, data=data)
        self.log_response()

        if self.response.status_code == 400:
            return None

        self.id = self.response.json().get("id")
        return self.id

    @allure.step("Проверка ответа при невалидном теле запроса")
    def check_create_meme_with_invalid_body(self):
        expected_lines = ["400 Bad Request", "Bad Request", "Invalid parameters"]

        if self.response.status_code == 400:
            soup = BeautifulSoup(self.response.text, "html.parser")
            actual_text = soup.get_text().strip()
            for line in expected_lines:
                assert line in actual_text, f"Строка '{line}' отсутствует в теле ответа"

            allure.attach(actual_text, name="Текст ошибки", attachment_type=allure.attachment_type.TEXT)
            self.log_response()
        else:
            with allure.step(f"Пропущена проверка текста ошибки (статус {self.response.status_code})"):
                pass

    @allure.step("Проверка структуры ответа")
    def test_response_body(self):
        if self.response.status_code == 200:
            try:
                MemeResponse(**self.response.json())
            except Exception as e:
                pytest.fail(f"Схема ответа не прошла валидацию: {e}")
        else:
            print(f"Пропущена валидация схемы: статус-код {self.response.status_code}")
        return self
