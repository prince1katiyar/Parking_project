

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, database
from .database import SessionLocal, engine, create_db_and_tables


create_db_and_tables()

app = FastAPI(title="Parking Management API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parking-slots/", response_model=schemas.ParkingSlotResponse, tags=["Parking Slots"])
def create_parking_slot_endpoint(slot: schemas.ParkingSlotCreate, db: Session = Depends(get_db)):
    return crud.create_parking_slot(db=db, slot=slot)

@app.get("/parking-slots/", response_model=List[schemas.ParkingSlotResponse], tags=["Parking Slots"])
def read_parking_slots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    slots = crud.get_parking_slots(db, skip=skip, limit=limit)
    return slots

@app.post("/get-parking-spots/", response_model=List[schemas.ParkingSlotResponse], tags=["Parking Search & Booking"])
def search_parking_spots_endpoint(search_params: schemas.ParkingSearchRequest, db: Session = Depends(get_db)):
    """
    Search for available parking spots based on vehicle type, location, slot type, and duration.
    Note: duration is used by the agent to decide, but not directly by this SQL query for availability.
    The agent should ensure the user wants a slot for a certain duration.
    """
    available_slots = crud.find_available_slots(db=db, search_params=search_params)
    if not available_slots:

        return []
    return available_slots

@app.post("/book-parking/", response_model=schemas.BookingResponse, tags=["Parking Search & Booking"])
def book_parking_endpoint(booking_request: schemas.BookingCreate, db: Session = Depends(get_db)):
    """
    Book a parking spot.
    Requires slot_id, user_id (can be a session_id), vehicle_number, and duration_hours.
    """

    booking = crud.create_booking(db=db, booking_data=booking_request)
    if not booking:
        raise HTTPException(status_code=400, detail="Failed to book parking spot. Slot might be unavailable or invalid.")


    return booking 


@app.get("/bookings/{booking_id}", response_model=schemas.BookingResponse, tags=["Bookings"])
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@app.get("/user-bookings/{user_id}", response_model=List[schemas.BookingResponse], tags=["Bookings"])
def read_user_bookings(user_id: str, db: Session = Depends(get_db)):
    bookings = crud.get_user_bookings(db, user_id=user_id)
    if not bookings:
        return []
    return bookings


@app.get("/health")
def health_check():
    return {"status": "ok"}













