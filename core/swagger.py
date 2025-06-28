from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from app.schemas.user_schema import UserSchema

spec = APISpec(
    title="Hackaton Backend API",
    version="1.0.0",
    openapi_version="3.0.2",
    info={"description": "Documentación generada automáticamente"},
    plugins=[MarshmallowPlugin()],
)

# Registrar schemas automáticamente
spec.components.schema("User", schema=UserSchema)
