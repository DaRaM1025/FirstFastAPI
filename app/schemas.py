from datetime import datetime
from random import randint
from pydantic import BaseModel, Field
from app.database.models import ShipmentStatus


def random_destination():
    return randint(11000, 11999)


##Used like base class to extend user face data, hide sensitive data to users
class ShipmentBase(BaseModel):
    content: str = Field(
        max_length=100, min_length=1, description=" defines the content of the shipment"
    )
    weight: float = Field(
        le=30, ge=0.1, description="defines the weight of shipment in Kg"
    )
    # Field defaults: Use 'default' for static immutable values.
    # Use 'default_factory' (callable) for mutable types (list, dict) to avoid shared references across instances.
    # default_factory also runs per-instance, perfect for UUIDs/timestamps.
    destination: int | None = Field(
        default_factory=random_destination,
        description="the zipcode of the destination place",
    )

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentStatusUpdate(BaseModel):
    status : ShipmentStatus | None = Field(
    description=" defines the status of the shipment", default= None
    )
    estimated_delivery: datetime | None = Field(default=None)

     

