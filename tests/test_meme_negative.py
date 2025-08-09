import pytest
import allure
from conftest import get_meme_endpoint, auth_endpoint, meme_id
from TEST_DATA import NEGATIVE_MEME


@allure.epic("Негативные кейсы")
class TestMemeNegative:

    @allure.title("Авторизация с невалидным токеном")
    @allure.feature("Авторизация")
    def test_authorize_invalid_token(self, auth_endpoint):
        auth_endpoint.authorize_invalid_token()
        auth_endpoint.check_status_code(404)
        auth_endpoint.assert_html_error_response_with_invalid_token()

    @allure.title("Авторизация с пустым токеном")
    @allure.feature("Авторизация")
    def test_authorize_empty_token(self, auth_endpoint):
        auth_endpoint.authorize_empty_token()
        auth_endpoint.check_status_code(404)
        auth_endpoint.assert_html_error_response_with_empty_token()

    @allure.title("Получение всех мемов с невалидным и пустым токеном")
    @allure.feature("Получение мемов")
    @pytest.mark.parametrize("token_type", ["invalid", "empty"])
    def test_get_all_memes_with_bad_token(self, token_type, get_meme_endpoint):
        if token_type == "invalid":
            get_meme_endpoint.get_meme_with_invalid_token()
        else:
            get_meme_endpoint.get_meme_with_empty_token()
        get_meme_endpoint.check_status_code(401)

    @allure.title("Получение одного мема с невалидным и пустым токеном")
    @allure.feature("Получение мема по ID")
    @pytest.mark.parametrize("token_type", ["invalid", "empty"])
    def test_get_single_meme_with_bad_token(self, token_type, meme_id, get_meme_endpoint):
        if token_type == "invalid":
            get_meme_endpoint.get_meme_with_invalid_token()
        else:
            get_meme_endpoint.get_meme_with_empty_token()
        get_meme_endpoint.check_status_code(401)

    @allure.title("Получение несуществующего мема")
    @allure.feature("Получение мема по ID")
    def test_get_meme_with_nonexistent_id(self, auth_token, get_meme_endpoint):
        get_meme_endpoint.get_meme_with_nonexistent_id(auth_token)
        get_meme_endpoint.check_status_code(404)

    @allure.title("Создание нового мема с невалидными данными")
    @allure.feature("Создание мема")
    def test_create_invalid_meme(self, create_meme_endpoint, auth_token):
        create_meme_endpoint.create_invalid_meme(token=auth_token, data=NEGATIVE_MEME)
        create_meme_endpoint.check_status_code(400)
        create_meme_endpoint.check_create_meme_with_invalid_body()
