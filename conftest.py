import pytest
import allure
from Endpoints.auth_token import AuthToken
from Endpoints.create_meme import CreateMeme
from Endpoints.get_meme import GetMeme
from Endpoints.update_meme import UpdateMeme
from Endpoints.delete_meme import DeleteMeme
from TEST_DATA import CREATE_MEME, NEGATIVE_MEME


@allure.title('Создание токена авторизации')
@pytest.fixture(scope="session")
def auth_token():
    client = AuthToken()
    token_str = client.create_token()
    assert token_str and isinstance(token_str, str) and len(token_str) > 10
    return token_str


@pytest.fixture()
def create_meme_endpoint():
    return CreateMeme()


@pytest.fixture()
def get_meme_endpoint():
    return GetMeme()


@pytest.fixture()
def update_meme_endpoint():
    return UpdateMeme()


@pytest.fixture()
def delete_meme_endpoint():
    return DeleteMeme()


@pytest.fixture()
def test_meme_id(auth_token, create_meme_endpoint, delete_meme_endpoint):
    meme_id = create_meme_endpoint.create_meme(token=auth_token, data=CREATE_MEME)
    yield meme_id
    try:
        delete_meme_endpoint.delete_meme(meme_id=meme_id, token=auth_token)
    except Exception:
        pass
