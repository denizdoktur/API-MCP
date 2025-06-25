from pydantic import BaseModel


class TextReaderRequest(BaseModel):
    parameters: dict