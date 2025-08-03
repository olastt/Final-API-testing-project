import allure
from .base_endpoint import Endpoint


class DeleteMeme(Endpoint):
    def __init__(self):
        super().__init__()
        self.api_url = "http://167.172.172.115:52355"

    @allure.step("Удаление мема")
    def delete_meme(self, meme_id, token=None):
        self.send_request(method="DELETE", endpoint="meme", meme_id=meme_id, token=token)
        self.log_response()
