import json
import typing
from typing import Dict, Any
import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

Response = requests.models.Response


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class LoginPayload:
    device_id: str
    email: str
    password: str
    captcha: Any
    captchaSubstitute: Any


class FTX:
    host: str = "https://ftx.us"

    def login(self, device_id: str, email: str, password: str):
        # s = requests.Session()
        # s.headers.update({'referer': })
        p: LoginPayload = LoginPayload(device_id, email, password, None, None)
        data = p.to_json()
        d = json.loads(data)
        r: Response = requests.post(self.host + '/api/users/login', json=p.to_dict())
        print(r.text)

