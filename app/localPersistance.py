import json

from app.schemas import Shipment

file = "./shipments.json"

shipments= {}

with open(file) as json_file:
    data = json.load(json_file)

    shipments = {
    int(shipment_id): Shipment(**shipment_data)
    for shipment_id, shipment_data in data.items()
}


def save():

    serializable = {
        shipment_id: shipment.model_dump()
        for shipment_id, shipment in shipments.items()
    }
    with open (file, "w") as json_file:
        json.dump( serializable, json_file, indent=2 )