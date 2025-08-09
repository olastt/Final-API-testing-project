import allure
from Endpoints.get_meme import GetMeme
from TEST_DATA import VALID_MEME
from conftest import get_meme_endpoint, auth_endpoint, meme_id


@allure.epic("Позитивные кейсы")
class TestMemePositive:

    @allure.title("Создание токена")
    @allure.feature("Авторизация")
    def test_create_token(self, auth_endpoint):
        auth_endpoint.create_token()
        auth_endpoint.check_response_in_body()
        auth_endpoint.check_token_is_string()
        auth_endpoint.assert_response_match_payload()

    @allure.title("Авторизация с валидным токеном")
    @allure.feature("Авторизация")
    def test_authorize_valid_token(self, auth_endpoint, auth_token):
        auth_endpoint.authorize_valid_token(auth_token)
        auth_endpoint.check_status_code(200)
        auth_endpoint.assert_text_in_response("Token is alive. Username is")

    @allure.title("Получение всех мемов с валидным токеном")
    @allure.feature("Получение мемов")
    def test_get_all_memes(self, auth_token, get_meme_endpoint):
        get_meme_endpoint.get_all_memes(auth_token)
        get_meme_endpoint.check_status_code(200)
        get_meme_endpoint.check_response_body()

    @allure.title("Получение мема по ID")
    @allure.feature("Получение мема по ID")
    def test_get_meme_by_id(self, auth_token, meme_id, get_meme_endpoint):
        get_meme_endpoint.get_meme_by_id(meme_id=meme_id, token=auth_token)
        get_meme_endpoint.check_status_code(200)
        get_meme_endpoint.assert_id_in_meme(expected_meme_id=meme_id)

    @allure.title("Создание нового мема с валидными данными")
    @allure.feature("Создание мема")
    def test_create_valid_meme(self, create_meme_endpoint, auth_token):
        create_meme_endpoint.create_valid_meme(token=auth_token, data=VALID_MEME)
        create_meme_endpoint.check_status_code(200)
        create_meme_endpoint.check_response_body()

    @allure.title("Изменение мема")
    @allure.feature("Изменение мема")
    def test_update_meme(self, update_meme_endpoint, auth_token, meme_id):
        update_meme_endpoint.update_meme(meme_id=meme_id, token=auth_token)
        update_meme_endpoint.check_status_code(200)
        update_meme_endpoint.check_updated_data(meme_id=meme_id,
                                                token=auth_token,
                                                expected_data=update_meme_endpoint.updated_data)

    @allure.title("Удаление мема")
    @allure.feature("Удаление мема")
    def test_delete_meme(self, delete_meme_endpoint, auth_token, meme_id):
        delete_meme_endpoint.delete_meme(meme_id=meme_id, token=auth_token)
        delete_meme_endpoint.check_status_code(200)

        # Проверяем, что мем больше не существует
        get_meme = GetMeme()
        get_meme.get_meme_by_id(meme_id=meme_id, token=auth_token)
        get_meme.check_status_code(404)
