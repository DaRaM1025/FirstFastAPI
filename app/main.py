from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import Shipment, ShipmentCreate, ShipmentStatus, ShipmentStatusUpdate

app = FastAPI()
shipments: dict[int, Shipment] = {
    1204: Shipment(
        content="laptop",
        weight=12.5,
        status=ShipmentStatus.delayed,
        destination_id=11001,
    ),
    1205: Shipment(
        content="phone", weight=0.5, status=ShipmentStatus.delayed, destination_id=11002
    ),
    1206: Shipment(
        content="books", weight=5.2, status=ShipmentStatus.pending, destination_id=11003
    ),
    1207: Shipment(
        content="furniture",
        weight=25.0,
        status=ShipmentStatus.in_transit,
        destination_id=11004,
    ),
    1208: Shipment(
        content="clothing",
        weight=3.0,
        status=ShipmentStatus.delayed,
        destination_id=11005,
    ),
    1209: Shipment(
        content="camera",
        weight=1.4,
        status=ShipmentStatus.delivered,
        destination_id=11006,
    ),
    1210: Shipment(
        content="monitor",
        weight=7.1,
        status=ShipmentStatus.in_transit,
        destination_id=11007,
    ),
    1211: Shipment(
        content="mouse", weight=0.2, status=ShipmentStatus.pending, destination_id=11008
    ),
    1212: Shipment(
        content="keyboard",
        weight=1.0,
        status=ShipmentStatus.delivered,
        destination_id=11009,
    ),
    1213: Shipment(
        content="printer",
        weight=9.3,
        status=ShipmentStatus.in_transit,
        destination_id=11010,
    ),
    1214: Shipment(
        content="headphones",
        weight=0.4,
        status=ShipmentStatus.pending,
        destination_id=11011,
    ),
}


##this way is the recommended one to stablish a model as a response, using ->
# only the IDE will know about the return. So better use both
#
# Only IGNORE the response_model statement when the endpoint return a variable
# unnecesary to validate.
@app.get("/shipment/latest", response_model=Shipment)
def get_latest_shipment() -> Shipment:
    if not shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    latest_id = max(shipments.keys())
    return shipments[latest_id]


@app.get("/shipment/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int) -> Shipment:
    if shipment_id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipments[shipment_id]


@app.get("/shipments")
def get_all_shipments() -> dict:
    if not shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not shipments registered"
        )
    return shipments


@app.get("/shipments/filter")
def get_filtered_shipments(
    byStatus: str | None = None, byContent: str | None = None
) -> list:
    filtered_shipments = list(shipments.values())

    if byStatus:
        filtered_shipments = [s for s in filtered_shipments if s.status == byStatus]
    if byContent:
        filtered_shipments = [
            shipment for shipment in filtered_shipments if shipment.content == byContent
        ]
    if not filtered_shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not matching results"
        )
    return filtered_shipments


@app.post("/shipment")
def post_shipments(data: ShipmentCreate) -> dict[str, int]:
    id = max(shipments.keys()) + 1
    ## use the incoming dict to construct a shipment object, the ** operator
    # extract the dict content as variables. 
    shipment = Shipment(**data.model_dump())
    shipments[id] = shipment
    return {"id": id}


##Updating all atributtes of shipment via query parameter
## the use of query parameters shall be specificly for GET request, dont use in others METHODS.
# when requires to use lot of parameters use a body request.
# @app.put("/shipment/{shipment_id}")
# def put_shipment_data(shipment_id: int, shipment_name : str, shipment_status: str, shipment_destination: str):
#     shipment = shipments[shipment_id]
#     if shipment:
#         shipment["name"] = shipment_name
#         shipment["status"] = shipment_status
#         shipment["destination"] = shipment_destination
#         return shipment
#     raise HTTPException(
#         status_code = status.HTTP_404_NOT_FOUND,
#         detail= "Not found shipment"
#     )


# PUT = full resource replacement with strict validation (FastAPI + Pydantic).
# All required fields must be present and correctly typed, otherwise HTTP 422.
# PATCH is the correct choice for partial updates.
@app.put("/shipment/{shipment_id}", response_model=ShipmentCreate)
def put_shipment_data_from_body(shipment_id: int, body: ShipmentCreate):
    shipment = shipments.get(shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found shipment"
        )
    ## updated get the new values from body and keep the unupdated values from shipment
    #in this case status still being "received"
    updated = shipment.model_copy(update=body.model_dump())

    shipments[shipment_id] = updated
    return updated


@app.patch("/shipment/{shipment_id}", response_model=Shipment)
def patch_shipment_status(
    shipment_id: int, shipment_status: ShipmentStatusUpdate
) -> Shipment:
    shipment = shipments.get(shipment_id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found shipment"
        )

    shipment.status = shipment_status.status
    return shipment


@app.delete("/shipment")
def delete_shipment(shipment_id: int) -> Shipment:
    shipment = shipments.get(shipment_id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found shipment"
        )

    shipments.pop(shipment_id)
    return shipment


@app.get("/scalar", include_in_schema=False)
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
