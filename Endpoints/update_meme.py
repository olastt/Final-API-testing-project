import json
import allure
import os

from Endpoints.get_meme import GetMeme
from Endpoints.base_endpoint import Endpoint
from dotenv import load_dotenv


class UpdateMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.token = None
        self.api_url = "http://167.172.172.115:52355"
        self.headers = {"Content-Type": "application/json"}
        self.updated_data = None

    @allure.step("Изменение мема")
    def update_meme(self, meme_id, token=None):
        self.updated_data = {
            "id": int(meme_id),
            "text": "update",
            "url": "update",
            "tags": ["one", "update"],
            "info": {"colors": ["update", "black", "white"]}
        }
        self.send_request(method="PUT", endpoint="meme", meme_id=meme_id, token=token, data=self.updated_data)
        self.log_response()

    @allure.step("Проверка мема после обновления")
    def check_updated_data(self, meme_id, expected_data=None, token=None):
        # Используем переданный токен, если он есть, иначе берем self.token
        token_to_use = token or self.token

        # Получаем текущие данные мема с актуальным токеном
        self.send_request(method="GET", endpoint=f"/meme/{meme_id}", token=token_to_use)
        self.log_response()
        response_data = self.response.json()

        response_data["id"] = int(response_data["id"])

        data_check = expected_data or self.updated_data

        with allure.step("Сравнение всех полей после обновления"):
            allure.attach(
                json.dumps(response_data, indent=2, ensure_ascii=False),
                name="Фактические данные",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                json.dumps(data_check, indent=2, ensure_ascii=False),
                name="Ожидаемые данные",
                attachment_type=allure.attachment_type.JSON
            )

            for key in data_check.keys():
                assert key in response_data, f"Поле '{key}' отсутствует в полученных данных."
                assert response_data[key] == data_check[key], f"Значение поля '{key}' отличается от ожидаемого."
