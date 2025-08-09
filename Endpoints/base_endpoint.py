import allure
import requests
import json


class Endpoint:
    def __init__(self):
        self.api_url = None
        self.api_token = None
        self.headers = None
        self.response = None

    @allure.step("Отправка HTTP-запроса")
    def send_request(self, method, endpoint, meme_id=None, token=None, headers=None, data=None):
        """
        Универсальный метод для отправки HTTP-запросов.
        """
        with allure.step("Формирование URL запроса"):
            base = self.api_url.rstrip('/')
            path = endpoint.lstrip('/')
            url = f"{base}/{path}"
            if meme_id is not None:
                url += f"/{meme_id}"

        with allure.step("Подготовка заголовков"):
            request_headers = {}
            if self.headers:
                request_headers.update(self.headers)
            if headers:
                request_headers.update(headers)

            if token == "":
                request_headers["Authorization"] = ";"
            elif token is not None:
                token_str = token.token if hasattr(token, 'token') else token
                request_headers["Authorization"] = f"{token_str}"

        with allure.step("Формирование cURL команды"):
            curl_parts = [f"curl -X {method.upper()} '{url}'"]
            for key, value in request_headers.items():
                curl_parts.append(f"-H '{key}: {value}'")
            if data:
                curl_parts.append(f"-d '{json.dumps(data)}'")
            curl_command = " \\\n  ".join(curl_parts)
            allure.attach(curl_command, name="cURL запроса", attachment_type=allure.attachment_type.TEXT)

        with allure.step(f"Выполнение запроса: {method.upper()}"):
            try:
                if method.upper() == "GET":
                    self.response = requests.get(url, headers=request_headers)
                elif method.upper() == "POST":
                    self.response = requests.post(url, headers=request_headers, json=data)
                elif method.upper() == "PUT":
                    self.response = requests.put(url, headers=request_headers, json=data)
                elif method.upper() == "DELETE":
                    self.response = requests.delete(url, headers=request_headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                return self.response
            except Exception as e:
                raise ValueError(f"Request failed: {str(e)}")

    @allure.step("Логирование ответа")
    def log_response(self):
        """
        Прикрепляет тело и статус ответа к отчету Allure.
        """
        try:
            json_str = json.dumps(self.response.json(), indent=2, ensure_ascii=False)
            allure.attach(json_str, name="Тело ответа (JSON)", attachment_type=allure.attachment_type.JSON)
        except Exception:
            allure.attach(self.response.text, name="Тело ответа (text)", attachment_type=allure.attachment_type.TEXT)

    @allure.step("Проверка статус-кода ответа")
    def check_status_code(self, expected_status_code):
        """
        Проверяет, что статус-код ответа совпадает с ожидаемым.
        """
        actual_status = self.response.status_code
        with allure.step(f"Ожидаемый статус: {expected_status_code}, полученный: {actual_status}"):
            assert actual_status == expected_status_code, (
                f"Ожидался статус-код {expected_status_code}, "
                f"но получен {actual_status}. Ответ: {self.response.text}"
            )
