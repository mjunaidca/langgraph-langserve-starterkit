from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel


class Data(BaseModel):
    messages: list[dict]
    summary: Optional[str] = None