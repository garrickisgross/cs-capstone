from pydantic import BaseModel


class OptimizationSummaryData(BaseModel):
    algorithm: str
    order_count: int
    original_distance: float
    optimized_distance: float
    distance_saved: float


class OptimizationOrderItem(BaseModel):
    id: str
    address: str
    city: str
    st: str
    description: str
    latitude: float
    longitude: float
    optimized: bool
    stop_number: int | None = None


class OptimizationOrdersListData(BaseModel):
    title: str
    orders: list[OptimizationOrderItem]
    summary: OptimizationSummaryData | None = None
    empty_message: str = "No orders available."


class OptimizationPageData(BaseModel):
    orders_list: OptimizationOrdersListData
    optimize_url: str
    message: str = "Optimize"
