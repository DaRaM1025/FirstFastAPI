from enum import Enum
from random import randint

from pydantic import BaseModel, Field

def random_destination():
    return randint(11000, 11999)

##Field allows to create validation and auto update docs
##BaseModel allows to define a base class working like a mirror for docs and validations, docs auto-recognize the request body
class ShipmentStatus(str, Enum):
    delayed = "delayed"
    in_transit = "in transit" 
    pending = "pending"
    delivered = "delivered"    
    received = "received"
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
    destination_id: int | None = Field(
        default_factory=random_destination,
        description="the zipcode of the destination place",
    )

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentStatusUpdate(BaseModel):
    status : ShipmentStatus = Field(
    description=" defines the status of the shipment"
    )

##Used to store data and retrive data using GET Methods
class Shipment(ShipmentBase):
    status : ShipmentStatus = Field(
        description=" defines the status of the shipment", 
        default= ShipmentStatus.received
    )
         

