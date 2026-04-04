from pydantic import BaseModel


class OrderFormElement(BaseModel):
    name: str
    input_type: str
    help_text: str


class OrdersPageData(BaseModel):
    elements: list[OrderFormElement]
    url: str


class CreateOrderInput(BaseModel):
    address: str
    city: str
    st: str
    description: str | None = None


class OrderCreatedMessage(BaseModel):
    message: str
    success: bool


class StoredOrder(BaseModel):
    id: str
    address: str
    city: str
    st: str
    description: str
    latitude: float
    longitude: float
    optimized: bool = False

    def to_row(self) -> tuple[str, str, str, str, str, float, float, bool]:
        return (
            self.id,
            self.address,
            self.city,
            self.st,
            self.description,
            self.latitude,
            self.longitude,
            self.optimized,
        )
