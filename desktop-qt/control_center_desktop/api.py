from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


class ApiError(RuntimeError):
    pass


@dataclass
class ApiClient:
    base_url: str
    access_token: str | None = None
    timeout_s: int = 15

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def login(self, email: str, password: str) -> str:
        url = f"{self.base_url.rstrip('/')}/api/v1/auth/login/access-token"
        data = {"username": email, "password": password}
        resp = requests.post(url, data=data, timeout=self.timeout_s)
        if resp.status_code != 200:
            raise ApiError(f"Login failed ({resp.status_code}): {resp.text}")
        payload = resp.json()
        token = payload.get("access_token")
        if not token:
            raise ApiError("Login response missing access_token")
        self.access_token = token
        return token

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url.rstrip('/')}{path}"
        resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout_s)
        if resp.status_code >= 400:
            raise ApiError(f"GET {path} failed ({resp.status_code}): {resp.text}")
        return resp.json()

    def post(self, path: str, json_body: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url.rstrip('/')}{path}"
        resp = requests.post(url, headers=self._headers(), json=json_body, timeout=self.timeout_s)
        if resp.status_code >= 400:
            raise ApiError(f"POST {path} failed ({resp.status_code}): {resp.text}")
        return resp.json()

    def put(self, path: str, json_body: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url.rstrip('/')}{path}"
        resp = requests.put(url, headers=self._headers(), json=json_body, timeout=self.timeout_s)
        if resp.status_code >= 400:
            raise ApiError(f"PUT {path} failed ({resp.status_code}): {resp.text}")
        return resp.json()

    def download(self, path: str, out_path, params: dict[str, Any] | None = None) -> None:
        url = f"{self.base_url.rstrip('/')}{path}"
        with requests.get(url, headers=self._headers(), params=params, stream=True, timeout=self.timeout_s) as resp:
            if resp.status_code >= 400:
                raise ApiError(f"DOWNLOAD {path} failed ({resp.status_code}): {resp.text}")
            with open(out_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=1024 * 256):
                    if chunk:
                        f.write(chunk)
