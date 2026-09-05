from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AuthenticatedUser(BaseModel):
    user_id: UUID
    email: str
    role: str = "paciente"  # 'paciente' o 'doctor'
    nombre: Optional[str] = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True
    )
