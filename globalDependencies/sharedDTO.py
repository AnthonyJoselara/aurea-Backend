from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """
    DTO base para todas las entidades del sistema Áurea.
    Convierte automáticamente los nombres de campos a camelCase en las entradas y salidas HTTP,
    permitiendo que internamente en Python y en PostgreSQL se mantengan en snake_case.
    """
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        validate_assignment=True
    )
