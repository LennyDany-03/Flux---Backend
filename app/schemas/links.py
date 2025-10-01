from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, constr

CodeStr = constr(pattern=r"^[a-zA-Z0-9_-]{3,64}$")

class LinkBase(BaseModel):
    title: Optional[str] = Field(default=None)

class LinkCreate(LinkBase):
    code: CodeStr
    destination_url: HttpUrl

class LinkUpdate(BaseModel):
    destination_url: Optional[HttpUrl] = None
    title: Optional[str] = None
    is_active: Optional[bool] = None

class LinkOut(BaseModel):
    id: str
    code: str
    destination_url: str
    title: Optional[str] = None
    is_active: bool
    created_at: str
    updated_at: str
