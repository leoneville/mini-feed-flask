from pydantic.v1 import BaseModel


class DefaultResponse(BaseModel):
    msg: str


class DefaultErrorResponse(DefaultResponse):
    type_error: str
    msg_error: str
