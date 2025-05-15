

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base 
import datetime 

class ParkingSlot(Base): 
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    slot_type = Column(String)
    vehicle_type = Column(String)
    is_available = Column(Boolean, default=True)
    price_per_hour = Column(Float)

    bookings = relationship("Booking", back_populates="slot")

class Booking(Base): 
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("parking_slots.id"))
    user_id = Column(String, index=True)
    vehicle_number = Column(String)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    duration_hours = Column(Integer)
    total_cost = Column(Float)
    is_confirmed = Column(Boolean, default=False)

    slot = relationship("ParkingSlot", back_populates="bookings")