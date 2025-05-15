

from .database import SessionLocal, create_db_and_tables 
from .models import ParkingSlot 
from .schemas import ParkingSlotCreate
from .crud import create_parking_slot

def init_db():

    print("Ensuring database tables are created...")
    create_db_and_tables() 
    print("Database tables checked/created.")
 
    db = SessionLocal()
    
    try:
    
        if db.query(ParkingSlot).count() == 0:
            print("Populating initial parking slot data (all will be initially available by default)...")
            slots_data = [
                ParkingSlotCreate(location="Downtown Mall", slot_type="covered", vehicle_type="car", price_per_hour=5.0),
                ParkingSlotCreate(location="Downtown Mall", slot_type="open", vehicle_type="car", price_per_hour=4.0),
                ParkingSlotCreate(location="Downtown Mall", slot_type="covered", vehicle_type="two-wheeler", price_per_hour=2.0),
                ParkingSlotCreate(location="Airport North", slot_type="long-term", vehicle_type="car", price_per_hour=3.0),
                ParkingSlotCreate(location="Airport North", slot_type="ev_charging", vehicle_type="car", price_per_hour=6.0),
                ParkingSlotCreate(location="City Center Plaza", slot_type="covered", vehicle_type="suv", price_per_hour=7.0),
                ParkingSlotCreate(location="City Center Plaza", slot_type="open", vehicle_type="two-wheeler", price_per_hour=1.5),
                ParkingSlotCreate(location="Tech Park West", slot_type="covered", vehicle_type="car", price_per_hour=4.5),
                ParkingSlotCreate(location="Tech Park West", slot_type="ev_charging", vehicle_type="car", price_per_hour=6.5),
   
            ]
            
            for slot_data in slots_data:
                create_parking_slot(db=db, slot=slot_data)
            print("Initial data populated.")
        else:
            print("Database already contains data. Skipping population.")
    finally:
     
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    print("Script execution started: Initializing database and populating data...")
    init_db() 
    print("Script execution finished: Database initialization complete.")