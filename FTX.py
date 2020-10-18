import json
import typing
from typing import Dict, Any
import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
import os

Response = requests.models.Response
ftx_email = os.environ["FTX_EMAIL"]
ftx_pass = os.environ["FTX_PASSWORD"]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LoginPayload:
    device_id: str
    email: str
    password: str
    captcha: Any
    captchaSubstitute: Any


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class APIKeyPayload:
    external_referral_program: str
    subaccount_specific: bool


class FTX:
    host: str = "https://ftx.us"
    bearer_token: str = None
    device_id: Any = None

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def login(self, device_id: str, email: str, password: str):
        p: LoginPayload = LoginPayload(device_id, email, password, None, None)
        r: Response = requests.post(self.host + '/api/users/login', json=p.to_dict())
        r = r.json()
        success = r['success']

        if success is False:
            error = r['error']
            raise Exception(f'Could not login to FTX: {error}')

        self.bearer_token = r['result']['token']

    def do(self, endpoint: str, method: str, payload: Any=None) -> Response:
        if self.bearer_token is None:
            self.login(device_id=None, email=self.email, password=self.password)

        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        r: Response = None
        url = self.host + endpoint

        if method == 'GET':
            r = requests.get(url, headers=headers)

        if method == 'POST':
            r = requests.post(url, headers=headers, json=payload.to_dict())

        return r

    def get_api_keys(self):
        r: Response = self.do("/api/api_keys", "GET")

        print(r.json())

    def create_api_key(self):
        payload: APIKeyPayload = APIKeyPayload("", False)
        r: Response = self.do("/api/api_keys", "POST", payload)

        print(r.json())


ftx = FTX(email=ftx_email, password=ftx_pass)
ftx.create_api_key()
ftx.get_api_keys()
