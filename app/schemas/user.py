from pydantic import BaseModel


class UserPublic(BaseModel):
    id: int
    email: str
    role: str

    model_config = {"from_attributes": True}
