import allure
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

        soup = BeautifulSoup(self.response.text, "html.parser")
        actual_text = soup.get_text().strip()

        for line in expected_lines:
            assert line in actual_text, f"Строка '{line}' отсутствует в теле ответа"

        allure.attach(actual_text, name="Текст ошибки", attachment_type=allure.attachment_type.TEXT)
        self.log_response()

    @allure.step("Проверка структуры ответа")
    def test_response_body(self):
        try:
            # Парсим JSON-ответ с помощью Pydantic
            meme_response = MemeResponse(**self.response.json())
            print(f"Validated response: {meme_response}")

        except Exception as e:
            assert False, f"Ответ не соответствует ожидаемой структуре: {e}"

        response_json = self.response.json()

        # Проверка наличия ключей верхнего уровня
        assert "id" in response_json, "Ключ 'id' отсутствует"
        assert "info" in response_json, "Ключ 'info' отсутствует"
        assert "tags" in response_json, "Ключ 'tags' отсутствует"
        assert "text" in response_json, "Ключ 'text' отсутствует"
        assert "updated_by" in response_json, "Ключ 'updated_by' отсутствует"
        assert "url" in response_json, "Ключ 'url' отсутствует"

        # Проверка типов данных
        assert isinstance(response_json["id"], int), "Тип 'id' не является целым числом"
        assert isinstance(response_json["info"], dict), "Тип 'info' не является словарём"
        assert isinstance(response_json["tags"], list), "Тип 'tags' не является списком"
        assert isinstance(response_json["text"], str), "Тип 'text' не является строкой"
        assert isinstance(response_json["updated_by"], str), "Тип 'updated_by' не является строкой"
        assert isinstance(response_json["url"], str), "Тип 'url' не является строкой"
        self.log_response()
