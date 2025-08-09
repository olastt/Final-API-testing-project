import pytest
import allure
from Endpoints.auth_token import AuthToken
from Endpoints.create_meme import CreateMeme
from Endpoints.get_meme import GetMeme
from Endpoints.update_meme import UpdateMeme
from Endpoints.delete_meme import DeleteMeme
from TEST_DATA import VALID_MEME, NEGATIVE_MEME

@pytest.fixture(scope="session")
def auth_endpoint():
    return AuthToken()

@allure.title('Создание токена авторизации')
@pytest.fixture(scope="session")
def auth_token(auth_endpoint):
    token_str = auth_endpoint.create_token()
    auth_endpoint.check_status_code(200)
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


@pytest.fixture
def meme_id(auth_token, create_meme_endpoint, delete_meme_endpoint):
    meme_id = create_meme_endpoint.create_valid_meme(token=auth_token, data=VALID_MEME)
    yield meme_id
    try:
        delete_meme_endpoint.delete_meme(meme_id=meme_id, token=auth_token)
    except Exception:
        pass
