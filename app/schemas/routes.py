from pydantic import BaseModel


class RoutesPageData(BaseModel):
    data: list[tuple[str, str, str, str, str, str | None]]
