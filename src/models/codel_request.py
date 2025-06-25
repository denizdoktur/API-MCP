from pydantic import BaseModel


class CodeRequest(BaseModel):
    parameters: dict