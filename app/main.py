from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any
from .schemas import Shipment, ShipmentCreate, ShipmentStatus, ShipmentStatusUpdate
from .localPersistance import save, shipments
from .databaseV1 import Database

app = FastAPI()
db = Database()

shipments = shipments

##this way is the recommended one to stablish a model as a response, using ->
# only the IDE will know about the return. So better use both
#
# Only IGNORE the response_model statement when the endpoint return a variable
# unnecesary to validate.
@app.get("/shipment/latest", response_model=Shipment)
def get_latest_shipment():
    shipment = db.get_latest()
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    
    return shipment


@app.get("/shipment/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int):
    shipment = db.get_shipment_by_id(shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipment


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


@app.post("/shipment", response_model= None)
def post_shipments(data: ShipmentCreate) -> dict[str, int]:
    new_id = db.save(data)
    return {"id": new_id}


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
    save()
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
    save()
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
