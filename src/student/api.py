from core.base_api import BaseAPI, SResponse


class StudentAPI(BaseAPI):
    endpoint = "/students"

    @classmethod
    async def check_group_leadership(cls, user_id: int) -> bool:
        user = await StudentAPI.get(telegram_id=user_id)
        group_id = user.json[0]["group_id"]

        resp = await cls._request(
            "GET",
            f"{cls.api_url}/auth/students/check_group_leadership",
            json_data={"user_id": user_id, "group_id": group_id},
        )
        if json_data := resp.json:
            return bool(json_data.get("success"))
        return False


class GroupAPI(BaseAPI):
    endpoint = "/groups"

    @classmethod
    async def get_degrees(cls, institute: int) -> SResponse:
        resp = await cls.get(institute=institute)
        degrees = list({item.get("degree") for item in resp.json})

        resp.json = degrees
        return resp
