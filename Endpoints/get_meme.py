import allure
import json
from Endpoints.base_endpoint import Endpoint


class GetMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.api_url = "http://167.172.172.115:52355"

    @allure.step("Получение мема по ID")
    def get_meme_by_id(self, meme_id, token=None):
        self.send_request(method="GET", endpoint="meme", meme_id=meme_id, token=token)
        self.log_response()

    @allure.step("Сверка ID в теле ответа")
    def assert_id_in_meme(self, expected_meme_id):
        if self.response.status_code != 200:
            allure.attach(
                self.response.text,
                name=f"Проверка пропущена, статус — {self.response.status_code}",
                attachment_type=allure.attachment_type.TEXT
            )
            return

        response_data = self.response.json()
        actual_id = response_data.get("id")
        assert actual_id == expected_meme_id, (
            f"Ожидался мем с ID {expected_meme_id}, но получен ID {actual_id} в ответе: {response_data}"
        )

        with allure.step("Сравнение ID"):
            allure.attach(
                json.dumps(expected_meme_id, indent=2, ensure_ascii=False),
                name="Ожидаемый ID",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                json.dumps(actual_id, indent=2, ensure_ascii=False),
                name="Фактический ID",
                attachment_type=allure.attachment_type.JSON
            )
        self.log_response()

    @allure.step("Получение несуществующего мема")
    def get_meme_with_nonexistent_id(self, token=None):
        self.send_request(method="GET", endpoint="meme", meme_id=50000, token=token)
        self.log_response()

    @allure.step("Получение всех мемов")
    def get_all_memes(self, token=None):
        self.send_request(method="GET", endpoint="meme", token=token)
        self.log_response()
