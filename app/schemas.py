

from pydantic import BaseModel, Field
from typing import List, Optional
import datetime


class ParkingSlotBase(BaseModel):
    location: str
    slot_type: str
    vehicle_type: str
    price_per_hour: float
    is_available: Optional[bool] = True

class ParkingSlotCreate(ParkingSlotBase):
    pass

class ParkingSlotResponse(BaseModel):
    id: int
    location: str
    slot_type: str
    vehicle_type: str
    price_per_hour: float
    is_available: bool

    class Config:
        orm_mode = True

class BookingBase(BaseModel):
    slot_id: int
    user_id: str
    vehicle_number: str

    duration_hours: int

class BookingCreate(BookingBase):

    pass

class BookingResponse(BaseModel): 
    id: int
    slot_id: int
    user_id: str
    vehicle_number: str
    duration_hours: int
    start_time: datetime.datetime 
    end_time: datetime.datetime   
    total_cost: float
    is_confirmed: bool
    slot: ParkingSlotResponse

    class Config:
        orm_mode = True


class ParkingSearchRequest(BaseModel):
    vehicle_type: str
    location: str
    slot_type: Optional[str] = None
    date: Optional[str] = Field(None, description="Desired date for parking (e.g., YYYY-MM-DD, 'today', 'tomorrow'). LLM will interpret.")
    duration_hours: int


class AvailableLocationsResponse(BaseModel):
    locations: List[str]