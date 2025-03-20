from utils.api.base import BaseAPI, SResponse

class GroupAPI(BaseAPI):
    endpoint = '/groups'

    @classmethod
    async def get_degrees(cls, institute: int) -> SResponse:
        resp = await cls.get(institute=institute)
        degrees = list({item.get('degree') for item in resp.json})

        resp.json = degrees
        return resp


class InstituteAPI(BaseAPI):
    endpoint = '/institutes'
