from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import (
    create_booking,
    get_booking,
    get_bookings,
    cancel_booking
)
from app.core.database import get_db

router = APIRouter()

@router.post("/booking", response_model=BookingOut, status_code=201)
def create_booking_endpoint(booking: BookingCreate, db: Session = Depends(get_db)):
    new_booking = create_booking(db, booking)

    if not new_booking:
        raise HTTPException(status_code=409, detail="Этот слот занят")
    return new_booking


@router.get("/booking", response_model=list[BookingOut])
def get_bookings__endpoint(date_filter: date | None = Query(None,description="Фильтр по дате (YYYY-MM-DD)" ), db: Session = Depends(get_db)):
    return get_bookings(db, date_filter)


@router.get("/booking/{booking_id}",response_model=BookingOut )
def get_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
        booking = get_booking(db, booking_id)
        if not booking:
             raise HTTPException(status_code=404,detail="Booking not found")
        return booking


@router.delete("/booking/{booking_id}", response_model=BookingOut)
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
        booking = cancel_booking(db, booking_id)
        if not booking:
             raise HTTPException(status_code=404,detail="Booking not found")
        return booking
