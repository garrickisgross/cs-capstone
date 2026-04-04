from pydantic import BaseModel


class OptimizationOrderItem(BaseModel):
    id: str
    address: str
    city: str
    st: str
    description: str
    latitude: float
    longitude: float
    route_id: str | None = None


class OptimizationOrdersListData(BaseModel):
    title: str
    orders: list[OptimizationOrderItem]
    empty_message: str = "No orders available."


class OptimizationPageData(BaseModel):
    orders_list: OptimizationOrdersListData
    optimize_url: str
    message: str = "Optimize"
