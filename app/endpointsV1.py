from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

app = FastAPI()
shipments: dict[int, dict] = {
    1204: {"name": "Shipment 1", "status": "delivered", "destination": "New York"},
    1205: {"name": "Shipment 2", "status": "in transit", "destination": "Los Angeles"},
    1206: {"name": "Shipment 3", "status": "pending", "destination": "Chicago"},
    1207: {"name": "Shipment 4", "status": "awaiting pickup", "destination": "Houston"},
    1208: {"name": "Shipment 5", "status": "delayed", "destination": "Miami"},
    1209: {"name": "Shipment 6", "status": "out for delivery", "destination": "Seattle"},
    1210: {"name": "Shipment 7", "status": "returned", "destination": "Denver"},
    1211: {"name": "Shipment 8", "status": "delivered", "destination": "New York"},
    1212: {"name": "Shipment 9", "status": "in transit", "destination": "Los Angeles"},
    1213: {"name": "Shipment 10", "status": "pending", "destination": "Chicago"},
    1214: {"name": "Shipment 11", "status": "pending", "destination": "Chicago"},
    1215: {"name": "Shipment 12", "status": "delayed", "destination": "Miami"},
    1216: {"name": "Shipment 13", "status": "delayed", "destination": "Houston"},
    1217: {"name": "Shipment 14", "status": "out for delivery", "destination": "Seattle"},
    1218: {"name": "Shipment 15", "status": "out for delivery", "destination": "Seattle"},
    1219: {"name": "Shipment 16", "status": "returned", "destination": "Denver"},
    1220: {"name": "Shipment 17", "status": "returned", "destination": "Miami"}
}


@app.get("/shipment/latest")
def get_latest_shipment():
    id = max(shipments.keys())
    if shipments:
        return shipments[id]
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail = "Shipment not found"
    )
@app.get("/shipment/{shipment_id}")
def get_shipment(shipment_id: int):
    shipment = shipments.get(shipment_id)
    if shipment:
        return shipment
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail = "Shipment not found"
    )
@app.get("/shipments")
def get_all_shipments()-> dict:
    if not shipments:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Not shipments registered"
        )
    return shipments

@app.get("/shipments/filter")
def get_filtered_shipments(byStatus : str | None = None, byDestination : str | None = None) -> list:
    filtered_shipments = list(shipments.values())

    if byStatus:
        filtered_shipments = [shipment for shipment in filtered_shipments  if shipment.get("status")== byStatus]
    if byDestination:
        filtered_shipments = [shipment for shipment in filtered_shipments  if shipment.get("destination")== byDestination]
    if not filtered_shipments:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= "Not matching results" )
    return filtered_shipments

@app.post("/shipment")
def post_shipments(data: dict):
    if not data:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail = "No data provided"
        )
    id = max(shipments.keys()) + 1
    shipments[id] = data
    return shipments[id]

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
@app.put("/shipment/{shipment_id}")
def put_shipment_data_from_body(shipment_id: int, body : dict):
    shipment = shipments.get(shipment_id)
    if shipment:
        shipment.update(body)
        return shipment 
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, 
            detail= "Not found shipment"
        )
    
@app.patch("/shipment/{shipment_id}")
def patch_shipment_data(shipment_id : int,
                         body: dict[str, Any]):
    shipment = shipments.get(shipment_id)

    if not shipment: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail= "Not found shipment")
    
    shipment.update(body)
    return shipment

@app.delete("/shipment")
def delete_shipment(shipment_id: int) -> dict[str, Any]:
    shipment = shipments.get(shipment_id)

    if not shipment: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
            detail= "Not found shipment")
    
    shipments.pop(shipment_id)
    return shipment

@app.get("/scalar", include_in_schema=False)
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
        )



