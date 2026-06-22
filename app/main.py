from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
app = FastAPI()


@app.get("/hello-world")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_api_reference_endpoint():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
        )
