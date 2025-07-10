from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class CurrentUser(BaseModel):
    sub: str
    roles: list[str] = []
