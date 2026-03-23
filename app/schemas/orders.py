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


class StoredOrder(BaseModel):
    id: str
    address: str
    city: str
    st: str
    description: str
    route_id: str | None = None

    def to_row(self) -> tuple[str, str, str, str, str, str | None]:
        return (
            self.id,
            self.address,
            self.city,
            self.st,
            self.description,
            self.route_id,
        )
