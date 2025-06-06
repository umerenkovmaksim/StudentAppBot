from core.base_api import BaseAPI, SResponse
from teacher.api import TeacherAPI


class LessonAPI(BaseAPI):
    endpoint = "/schedule/lessons"

    @classmethod
    async def get(cls, with_teacher: bool = False, **kwargs) -> SResponse:
        if kwargs.get("date"):
            kwargs["date"] = kwargs["date"].strftime("%Y-%m-%d")

        resp = await super().get(**kwargs)
        if with_teacher:
            for lesson in resp.json:
                if teacher_id := lesson.get("teacher_id"):
                    lesson["teacher"] = (await TeacherAPI.get_by_id(teacher_id)).json

        return resp


class InstituteAPI(BaseAPI):
    endpoint = "/institutes"
