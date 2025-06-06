import json

from aiohttp import ClientSession


class BaseAPI:
    api_url: str | None = None
    endpoint: str | None = None

    session: ClientSession | None = None

    @staticmethod
    async def __normalize_url(url: str) -> str:
        if url[-1] == "/":
            return url[:-1]
        return url

    @classmethod
    async def _request(
        cls,
        method: str,
        url: str,
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> "SResponse":
        async with cls.session.request(
            method,
            url,
            params=params,
            json=json_data,
        ) as response:
            try:
                return SResponse(
                    await response.json(),
                    None,
                    response.status,
                    response.ok,
                )
            except json.JSONDecodeError as e:
                return SResponse(None, e.msg, response.status, response.ok)

    @classmethod
    async def init(cls, api_url: str, token: str) -> None:
        cls.api_url = await cls.__normalize_url(api_url)
        cls.session = ClientSession()
        cls.session.headers.update({"Authorization": f"Bearer {token}"})

    @classmethod
    async def close(cls) -> None:
        cls.session.close()

    @classmethod
    async def get(cls, **kwargs) -> "SResponse":
        url = f"{cls.api_url}{cls.endpoint}"
        return await cls._request("GET", url, kwargs)

    @classmethod
    async def get_by_id(cls, id: int, **kwargs) -> "SResponse":
        url = f"{cls.api_url}{cls.endpoint}/{id}"
        return await cls._request("GET", url, kwargs)

    @classmethod
    async def post(cls, json_data: dict | None = None, **kwargs) -> "SResponse":
        url = f"{cls.api_url}{cls.endpoint}"
        return await cls._request("POST", url, kwargs, json_data)

    @classmethod
    async def patch(cls, id: int, **kwargs) -> "SResponse":
        url = f"{cls.api_url}{cls.endpoint}/{id}"
        return await cls._request("PATCH", url, json_data=kwargs)

    @classmethod
    async def delete(cls, id: int) -> "SResponse":
        url = f"{cls.api_url}{cls.endpoint}/{id}"
        return await cls._request("DELETE", url)


class SResponse:
    def __init__(self, json: dict, error: str | None, status: int, ok: bool):
        self.json = json
        self.error = error
        self.status = status
        self.ok = ok
