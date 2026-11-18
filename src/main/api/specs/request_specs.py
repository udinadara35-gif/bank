from src.main.api.configs.config import Config
import requests
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    _token = None
    @staticmethod
    def base_headers():
         return {
               "Content-Type": "application/json",
               "Accept": "application/json"
         }
# Здесь делаем запрос на сервер по авторизации
    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            RequestSpecs._token = token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception("Failed to login")

    @staticmethod
    def unauth_headers():
        return RequestSpecs.base_headers()

    @staticmethod
    def get_auth_headers():
        headers = RequestSpecs.base_headers()
        if RequestSpecs._token:
            headers["Authorization"] = f"Bearer {RequestSpecs._token}"
        return headers


