from utils.api.base import BaseAPI

class StudentAPI(BaseAPI):
    endpoint = '/students'

    @classmethod
    async def check_group_leadership(cls, user_id: int, group_id: int) -> bool:
        resp = await cls._request(
            'GET',
            f'{cls.api_url}/auth/students/check_group_leadership',
            json_data={'user_id': user_id, 'group_id': group_id},
        )
        if json_data := resp.json:
            return bool(json_data.get('success'))
        return False
