from pydantic import BaseModel


class OptimizationPageData(BaseModel):
    message: str = "Optimize"
