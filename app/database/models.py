from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


##Field allows to create validation and auto update docs
##BaseModel allows to define a base class working like a mirror for docs and validations, docs auto-recognize the request body
class ShipmentStatus(str, Enum):
    delayed = "delayed"
    in_transit = "in transit" 
    pending = "pending"
    delivered = "delivered"    
    received = "received"

##SQLModel also contains the BaseModel behavior, allowing to 
## use Field and data validation. 
class Shipment(SQLModel, table=True):
    ##__tablename__: <name>
    id: int = Field(default=None, primary_key= True)
    content: str
    weight: float = Field(le=30)
    destination: int
    status : ShipmentStatus
    estimated_delivery: datetime