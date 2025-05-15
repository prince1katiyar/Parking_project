

import httpx
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, List
import json
import datetime 

BASE_API_URL = "http://localhost:8000"


class ParkingSearchToolInput(BaseModel):
    vehicle_type: str = Field(description="Type of vehicle, e.g., 'car', 'two-wheeler', 'suv'.")
    location: str = Field(description="Desired parking location, e.g., 'Downtown Mall', 'Airport North'.")
    slot_type: Optional[str] = Field(None, description="Preferred slot type, e.g., 'covered', 'open', 'ev_charging'.")
    date: Optional[str] = Field(None, description="Desired date for parking (e.g., 'YYYY-MM-DD', 'today', 'tomorrow'). If not provided, implies current general availability.")
    duration_hours: int = Field(description="Desired parking duration in hours.")

class ParkingBookingToolInput(BaseModel):
    slot_id: int = Field(description="The ID of the parking slot to book.")
    user_id: str = Field(description="A unique identifier for the user or session (this should be the session_id).")
    vehicle_number: str = Field(description="The vehicle's registration number.")
    duration_hours: int = Field(description="The duration for which the parking is booked, in hours (this should be the same duration used for the search that found this slot).")

class GetAvailableLocationsForVehicleToolInput(BaseModel):
    vehicle_type: str = Field(description="Type of vehicle, e.g., 'car', 'two-wheeler'.")



class SearchParkingSpotsTool(BaseTool):
    name: str = "SearchParkingSpots"
    description: str = (
        "Use this tool to search for available parking spots. "
        "Provide vehicle_type, location, duration_hours, and optionally slot_type and date (e.g., 'today', 'YYYY-MM-DD'). "
        "Returns a list of currently available parking spots matching criteria or an empty list if none are found. "
        "Note: Current search checks general availability, not specific time-slot clashes for the given date."
    )
    args_schema: Type[BaseModel] = ParkingSearchToolInput

    def _run(self, vehicle_type: str, location: str, duration_hours: int, date: Optional[str] = None, slot_type: Optional[str] = None) -> str:
        print(f"DEBUG TOOL (SearchParkingSpotsTool): _run CALLED. vehicle_type='{vehicle_type}', location='{location}', duration_hours={duration_hours}, date='{date}', slot_type='{slot_type}'")
        try:
            payload = {
                "vehicle_type": vehicle_type.lower(),
                "location": location,
                "slot_type": slot_type.lower() if slot_type else None,
                "date": date, 
                "duration_hours": duration_hours
            }
            payload_cleaned = {k: v for k, v in payload.items() if v is not None} 
            print(f"DEBUG TOOL (SearchParkingSpotsTool): PAYLOAD SENT TO API: {payload_cleaned}")

            response = httpx.post(f"{BASE_API_URL}/get-parking-spots/", json=payload_cleaned)
            print(f"DEBUG TOOL (SearchParkingSpotsTool): API RESPONSE STATUS: {response.status_code}")
            raw_api_response_text = response.text
            print(f"DEBUG TOOL (SearchParkingSpotsTool): RAW API RESPONSE TEXT: {raw_api_response_text}")
            response.raise_for_status()
            results = response.json()

            if not results:
                print("DEBUG TOOL (SearchParkingSpotsTool): API returned empty list. No spots found by API.")
                return "No parking spots found matching your criteria for the specified details. You can try a different location or vehicle type."
            else:
                summary = (f"Successfully found {len(results)} parking spot(s) generally matching criteria for {vehicle_type} at {location} "
                           f"(date context: {date if date else 'any available day'}, duration: {duration_hours} hours). "
                           f"Details are in the following JSON. Please present these options to the user clearly:\n")
                output_for_agent = summary + json.dumps(results)
                print(f"DEBUG TOOL (SearchParkingSpotsTool): OUTPUT SENT TO AGENT: {output_for_agent}")
                return output_for_agent
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json().get("detail", e.response.text) if e.response else e.request.url
            status_code_info = f"(Status: {e.response.status_code})" if e.response else "(No response status)"
            print(f"DEBUG TOOL (SearchParkingSpotsTool): HTTPStatusError: {error_detail} {status_code_info}")
            return f"Error searching for parking spots: {error_detail} {status_code_info}"
        except Exception as e:
            print(f"DEBUG TOOL (SearchParkingSpotsTool): UNEXPECTED TOOL ERROR: {str(e)}")
            return f"An unexpected error occurred while searching for parking spots: {str(e)}"


class BookParkingSpotTool(BaseTool):
    name: str = "BookParkingSpot"
    description: str = (
        "Use this tool to book a specific parking spot AFTER it has been found and user has confirmed which slot_id to book and provided their vehicle_number. "
        "Requires slot_id, user_id (session_id), vehicle_number, and duration_hours (from the original search). "
        "Booking is assumed to be for the current time or the conceptually discussed date."
    )
    args_schema: Type[BaseModel] = ParkingBookingToolInput

    def _run(self, slot_id: int, user_id: str, vehicle_number: str, duration_hours: int) -> str:
        print(f"DEBUG TOOL (BookParkingSpotTool): _run CALLED. slot_id={slot_id}, user_id='{user_id}', vehicle_number='{vehicle_number}', duration_hours={duration_hours}")
        try:
            payload = {
                "slot_id": slot_id,
                "user_id": user_id,
                "vehicle_number": vehicle_number,
                "duration_hours": duration_hours
            }
            print(f"DEBUG TOOL (BookParkingSpotTool): PAYLOAD SENT TO API: {payload}")
            response = httpx.post(f"{BASE_API_URL}/book-parking/", json=payload)
            print(f"DEBUG TOOL (BookParkingSpotTool): API RESPONSE STATUS: {response.status_code}")
            raw_api_response_text = response.text
            print(f"DEBUG TOOL (BookParkingSpotTool): RAW API RESPONSE TEXT: {raw_api_response_text}")
            response.raise_for_status()
            booking_confirmation = response.json() 
            

            start_dt = datetime.datetime.fromisoformat(booking_confirmation['start_time'].replace('Z', '+00:00')) 
            end_dt = datetime.datetime.fromisoformat(booking_confirmation['end_time'].replace('Z', '+00:00'))
            
            confirmation_message = (
                f"Booking successful! Your parking for vehicle {booking_confirmation['vehicle_number']} "
                f"at Slot ID {booking_confirmation['slot']['id']} ({booking_confirmation['slot']['location']}) "
                f"is confirmed from {start_dt.strftime('%Y-%m-%d %I:%M %p %Z')} to {end_dt.strftime('%Y-%m-%d %I:%M %p %Z')} " # Added %Z for timezone
                f"({booking_confirmation['duration_hours']} hours). Total cost: ${booking_confirmation['total_cost']:.2f}. "
                f"Your Booking ID is {booking_confirmation['id']}."
            )
            print(f"DEBUG TOOL (BookParkingSpotTool): OUTPUT SENT TO AGENT: {confirmation_message}")
            return confirmation_message
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json().get("detail", e.response.text) if e.response else e.request.url
            status_code_info = f"(Status: {e.response.status_code})" if e.response else "(No response status)"
            print(f"DEBUG TOOL (BookParkingSpotTool): HTTPStatusError: {error_detail} {status_code_info}")
            return f"Error booking parking spot: {error_detail} {status_code_info}"
        except Exception as e:
            print(f"DEBUG TOOL (BookParkingSpotTool): UNEXPECTED TOOL ERROR: {str(e)}")
            return f"An unexpected error occurred while booking the parking spot: {str(e)}"

class GetAvailableLocationsForVehicleTool(BaseTool):
    name: str = "GetAvailableLocationsForVehicle"
    description: str = (
        "Use this tool to get a list of general locations where parking might be available "
        "for a specific vehicle_type. This is useful if the user asks 'Where can I park my car?' "
        "without specifying a particular location. It does not give specific slots, only location names."
    )
    args_schema: Type[BaseModel] = GetAvailableLocationsForVehicleToolInput

    def _run(self, vehicle_type: str) -> str:
        print(f"TOOL (GetAvailableLocationsForVehicleTool): _run CALLED. vehicle_type='{vehicle_type}'")
        try:
            if not vehicle_type:
                return "Error: Vehicle type is required to find available locations."
            response = httpx.get(f"{BASE_API_URL}/get-available-locations-for-vehicle/", params={"vehicle_type": vehicle_type.lower()})
            print(f"TOOL (GetAvailableLocationsForVehicleTool): API RESPONSE STATUS: {response.status_code}")
            raw_api_response_text = response.text
            print(f"TOOL (GetAvailableLocationsForVehicleTool): RAW API RESPONSE TEXT: {raw_api_response_text}")
            response.raise_for_status()
            data = response.json()
            locations = data.get("locations", [])
            if not locations:
                return f"I couldn't find any general locations with available parking for a {vehicle_type} right now."
            else:
                return (f"Based on current availability, you might find parking for a {vehicle_type} at the following locations: "
                        f"{', '.join(locations)}. If you'd like to search at one of these, please tell me the specific location, "
                        f"the date, and for how long you need parking.")
        except httpx.HTTPStatusError as e:
            error_detail = e.response.json().get("detail", e.response.text) if e.response else e.request.url
            status_code_info = f"(Status: {e.response.status_code})" if e.response else "(No response status)"
            print(f"DEBUG TOOL (GetAvailableLocationsForVehicleTool): HTTPStatusError: {error_detail} {status_code_info}")
            return f"Error getting available locations: {error_detail} {status_code_info}"
        except Exception as e:
            print(f"DEBUG TOOL (GetAvailableLocationsForVehicleTool): UNEXPECTED TOOL ERROR: {str(e)}")
            return f"An unexpected error occurred while getting available locations: {str(e)}"


search_parking_tool = SearchParkingSpotsTool()
book_parking_tool = BookParkingSpotTool()
get_available_locations_tool = GetAvailableLocationsForVehicleTool()

list_of_tools = [search_parking_tool, book_parking_tool, get_available_locations_tool]