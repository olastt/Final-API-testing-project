# Этот проект содержит набор **API-тестов** для тестирования сервиса

# Стек технологий:
- python
- pytest
- requests
- allure
- python-dotenv

## Основные возможности:
- Создание / обновление / удаление мемов
- Авторизация через токен
- Проверка статус-кодов и тела ответа
- Логирование в Allure
- Работа с `.env` файлами
- Поддержка параметризованных тестов

## Для работы с проектом:
Создайте .env из шаблона командой
```bash
cp .env.example .env
```
Заполните .env своими данными:
```bash
API_URL=http://your-api.com
API_NAME=your_api_name
TOKEN=your_token
```
Запустите автотесты:
```bash
pytest --alluredir=./allure-results
```
Для открытия отчета в Allure:
```bash
pytest allure serve ./allure-results
```