import json
from main import app

from fastapi.openapi.utils import get_openapi
openapi_schema = get_openapi(
    title=app.title,
    version=app.version,
    routes=app.routes,
)

with open("scripts/openapi.json", "w") as f:
    json.dump(openapi_schema, f, indent=2)