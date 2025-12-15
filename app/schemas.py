from datetime import datetime
from pydantic import BaseModel,Field

class BinCreate(BaseModel):
    name: str=Field(..., max_length=120)
    location:str | None = Field(None, max_length=255)

    warning_threshold: int = Field(default=80, ge=0, le=100)
    full_threshold: int = Field(default=95, ge=0, le=100)


class BinOut(BaseModel):
    id: int
    name: str
    location: str | None
    warning_threshold: int
    full_threshold: int
    current_level: int
    created_at: datetime

    class Config:
       from_attributes = True

class ReadingCreate(BaseModel):
    bin_id: int
    fill_percent: int = Field(..., ge=0, le=100)

class ReadingOut(BaseModel):
    id: int
    bin_id: int
    fill_percent: int
    created_at: datetime

    class Config:
        from_attributes = True

class AlertOut(BaseModel):
    id: int
    bin_id: int
    level: str
    status: str
    message: str | None
    created_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str  = Field(..., pattern="^(OPEN|ACK|RESOLVED)$")