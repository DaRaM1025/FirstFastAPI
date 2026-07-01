from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from rich import panel, print
from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from typing import Any

from app.database.models import Shipment
from .schemas import ShipmentCreate, ShipmentStatus, ShipmentStatusUpdate
from .database.session import SessionDep, create_all_tables

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    ##Use rich package to pretty print in console
    print(panel.Panel("Starded", border_style="green"))
    create_all_tables()
    # The `yield` keyword transforms the function into a generator, pausing its
    # execution at this line and returning control to the caller (the context manager).
    # The code block before `yield` runs when entering the context (startup).
    # Once the context block (the FastAPI app) finishes, execution resumes exactly
    # after this `yield` statement, running the teardown code (shutdown).
    yield
    ##Use rich package to pretty print in console
    print(panel.Panel("Stopped", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)





@app.get("/shipment/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int, session : SessionDep):
    shipment = session.get(Shipment, shipment_id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No shipments found"
        )
    return shipment




@app.post("/shipment", response_model=None)
def post_shipments(data: ShipmentCreate, session : SessionDep) -> dict[str, int]:
    new_shipment = Shipment(**data.model_dump(),
                            status= ShipmentStatus.received,
                            estimated_delivery= datetime.now() + timedelta(days=3))
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id": new_shipment.id}


@app.patch("/shipment/{shipment_id}", response_model=Shipment)
def patch_shipment_status(
    shipment_id: int, updated_shipment: ShipmentStatusUpdate, session: SessionDep
) -> Shipment:

    updated= updated_shipment.model_dump(exclude_none=True)
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Not data provided"
        )
    shipment = session.get(Shipment,shipment_id)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not found shipment"
        )
    shipment.sqlmodel_update(updated)

    session.add(shipment)
    session.commit()

    session.refresh(shipment)
    return shipment


@app.delete("/shipment")
def delete_shipment(shipment_id: int, session : SessionDep) -> dict[str, Any]:
    session.delete(
        session.get(Shipment, shipment_id)
    )

    session.commit()
    return {"detail": f"Shipment with id #{shipment_id} is deleted!"}


@app.get("/scalar", include_in_schema=False)
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
