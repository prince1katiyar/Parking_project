
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from typing import List 
from . import models, schemas
import datetime 


def get_parking_slot(db: Session, slot_id: int):
    return db.query(models.ParkingSlot).filter(models.ParkingSlot.id == slot_id).first()

def get_parking_slots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ParkingSlot).offset(skip).limit(limit).all()

def create_parking_slot(db: Session, slot: schemas.ParkingSlotCreate):
 
    db_slot = models.ParkingSlot(**slot.model_dump())

    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def find_available_slots(db: Session, search_params: schemas.ParkingSearchRequest):
    """
    Finds currently available slots.
    NOTE: The 'date' from search_params is NOT used for DB filtering in this version.
    This function checks general availability (ParkingSlot.is_available == True).
    A full time-based availability check would require comparing requested date/duration
    against start_time/end_time of existing bookings for each slot.
    """
    print(f"CRUD: Searching with params: vehicle_type='{search_params.vehicle_type}', "
          f"location='{search_params.location}', slot_type='{search_params.slot_type}', "
          f"date='{search_params.date}', duration='{search_params.duration_hours}'")

    query = db.query(models.ParkingSlot).filter(
        models.ParkingSlot.is_available == True,
        models.ParkingSlot.vehicle_type.ilike(search_params.vehicle_type),
        models.ParkingSlot.location.ilike(f"%{search_params.location}%")
    )
    
    if search_params.slot_type:
        query = query.filter(models.ParkingSlot.slot_type.ilike(search_params.slot_type))
    
    results = query.all()
    print(f"CRUD: Found {len(results)} generally available slots matching criteria (not yet time-filtered).")
    return results


def create_booking(db: Session, booking_data: schemas.BookingCreate):
    slot = get_parking_slot(db, booking_data.slot_id)
    if not slot:
        print(f"CRUD create_booking: Slot ID {booking_data.slot_id} not found.")
        return None
    if not slot.is_available:
        print(f"CRUD create_booking: Slot ID {booking_data.slot_id} is not generally available.")
        return None

    start_time = datetime.datetime.utcnow()
    end_time = start_time + datetime.timedelta(hours=booking_data.duration_hours)
    total_cost = slot.price_per_hour * booking_data.duration_hours

    db_booking = models.Booking(
        slot_id=booking_data.slot_id,
        user_id=booking_data.user_id,
        vehicle_number=booking_data.vehicle_number,
        start_time=start_time,
        end_time=end_time,
        duration_hours=booking_data.duration_hours,
        total_cost=total_cost,
        is_confirmed=True
    )
    
    slot.is_available = False
    
    db.add(db_booking)
    db.add(slot)
    db.commit()
    
    db.refresh(db_booking)
    db.refresh(slot)
    
    return db_booking

def get_booking(db: Session, booking_id: int):
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_user_bookings(db: Session, user_id: str) -> List[models.Booking]: # Added type hint for return
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).order_by(models.Booking.start_time.desc()).all()


def get_distinct_locations_for_vehicle_type(db: Session, vehicle_type: str) -> List[str]:
    print(f"CRUD (get_distinct_locations_for_vehicle_type): Searching for vehicle_type='{vehicle_type}'")
    query_result = db.query(distinct(models.ParkingSlot.location)).filter(
        models.ParkingSlot.is_available == True, # <--- Crucial filter
        models.ParkingSlot.vehicle_type.ilike(vehicle_type)
    ).all()
    locations = [location_tuple[0] for location_tuple in query_result]
    print(f"CRUD (get_distinct_locations_for_vehicle_type): Found locations: {locations}")
    return locations

