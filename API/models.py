from pydantic import BaseModel

class User(BaseModel):
    name: str
    family: str
    password: str
    age: int


class Delete(BaseModel):
    name: str