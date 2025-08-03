import allure
from Endpoints.base_endpoint import Endpoint


class GetMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.api_url = "http://167.172.172.115:52355"

    @allure.step("Получение мема по ID")
    def get_meme_by_id(self, meme_id, token=None):
        self.send_request(method="GET", endpoint="meme", meme_id=meme_id, token=token)
        self.log_response()

    @allure.step("Получение всех мемов")
    def get_all_memes(self, token=None):
        self.send_request(method="GET", endpoint="meme", token=token)
        self.log_response()
