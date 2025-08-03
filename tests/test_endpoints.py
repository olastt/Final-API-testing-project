import allure
import pytest

from Endpoints.auth_token import AuthToken
from Endpoints.create_meme import CreateMeme
from Endpoints.get_meme import GetMeme
from TEST_DATA import CREATE_MEME, NEGATIVE_MEME


class TestMemeMethods:

    @allure.title("Создание токена")
    @allure.epic("Авторизация")
    @allure.feature("Создание токена")
    def test_create_token(self):
        # Создается в фикстуре
        pass

    @allure.title("Авторизация")
    @allure.epic("Авторизация")
    @allure.feature("Авторизация")
    @allure.suite("Авторизация")
    @pytest.mark.parametrize("token_type, expected_status", [
        ("valid", 200),
        ("none", 404),
        ("invalid", 404)
    ])
    def test_authorize(self, auth_token, token_type, expected_status):
        client = AuthToken()
        client.token = auth_token
        client.authorize(token_type=token_type)
        client.check_status_code(expected_status)

    @allure.title("Получение всех мемов")
    @allure.epic("Получение мемов")
    @allure.feature("Получение мемов")
    @allure.suite("Получение мемов")
    @pytest.mark.parametrize("token_type, expected_status", [
        ("valid", 200),
        ("none", 401),
        ("empty", 401),
        ("invalid", 401)
    ])
    def test_get_all_memes(self, auth_token, get_meme_endpoint, token_type, expected_status):
        tokens = {
            "valid": auth_token,
            "none": None,
            "empty": "",
            "invalid": AuthToken().generate_invalid_token()
        }
        get_meme_endpoint.get_all_memes(token=tokens[token_type])
        get_meme_endpoint.check_status_code(expected_status)

    @allure.feature("Получение мема по id")
    @allure.suite("Получение мема по id")
    @pytest.mark.parametrize("token_type, expected_status", [
        ("valid", 200),
        ("none", 401),
        ("empty", 401),
        ("invalid", 401)
    ])
    def test_get_meme_by_id(self, auth_token, test_meme_id, get_meme_endpoint, token_type, expected_status):
        tokens = {
            "valid": auth_token,
            "none": None,
            "empty": "",
            "invalid": AuthToken().generate_invalid_token()
        }
        get_meme_endpoint.get_meme_by_id(meme_id=test_meme_id, token=tokens[token_type])
        get_meme_endpoint.check_status_code(expected_status)

    @allure.title("Создание нового мема")
    @allure.epic("Создание мема")
    @allure.feature("Создание нового мема")
    @allure.suite("Создание нового мема")
    @pytest.mark.parametrize("data, expected_status", [
        (CREATE_MEME, 200),
        (NEGATIVE_MEME, 400)
    ])
    def test_create_new_meme(self, create_meme_endpoint, auth_token, data, expected_status):
        create_meme_endpoint.create_meme(token=auth_token, data=data)
        create_meme_endpoint.check_status_code(expected_status)

    @allure.title("Изменение мема")
    @allure.epic("Изменение мема")
    @allure.feature("Изменение мема")
    @allure.suite("Изменение мема")
    def test_update_meme(self, update_meme_endpoint, auth_token, test_meme_id):
        update_meme_endpoint.update_meme(meme_id=test_meme_id, token=auth_token)
        update_meme_endpoint.check_status_code(200)
        update_meme_endpoint.check_updated_data(meme_id=test_meme_id,
                                                token=auth_token,
                                                expected_data=update_meme_endpoint.updated_data)

    @allure.title("Удаление мема")
    @allure.epic("Удаление мема")
    @allure.feature("Удаление мема")
    @allure.suite("Удаление мема")
    def test_delete_meme(self, delete_meme_endpoint, auth_token):
        # Сначала создаем мем, чтобы потом удалить
        meme_id = CreateMeme().create_meme(token=auth_token, data=CREATE_MEME)
        delete_meme_endpoint.delete_meme(meme_id=meme_id, token=auth_token)
        delete_meme_endpoint.check_status_code(200)

        # Проверяем, что мем больше не существует
        get_meme = GetMeme()
        get_meme.get_meme_by_id(meme_id=meme_id, token=auth_token)
        get_meme.check_status_code(404)
