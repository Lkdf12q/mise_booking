from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.schemas.booking import BookingCreate

def create_booking(db: Session, booking_data: BookingCreate): #Создание Брони
    existing_booking = db.query(Booking).filter(
        Booking.booking_date == booking_data.booking_date,
        Booking.booking_time == booking_data.booking_time,
        Booking.status == "active"
    ).first()
    if existing_booking: #Проверка на доступность брони
        return None
    
    new_booking = Booking( #перекладывание данных из Пайдентик схемы в ОРМ модель
        name=booking_data.name,
        phone=booking_data.phone,
        booking_date=booking_data.booking_date,
        booking_time=booking_data.booking_time,
        guests=booking_data.guests,
        status="active"
    )

    db.add(new_booking) #Добавление в БД
    db.commit()
    db.refresh(new_booking)

    return new_booking

def get_booking(db:Session, booking_id: int): #Получение одной брони по айди
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings(db:Session, date_filter: None): #Получение списка броней
    query = db.query(Booking)
    if date_filter:
        query = query.filter(Booking.booking_date == date_filter)
    return query.all()

def cancel_booking(db:Session, booking_id: int): #Отмена брони
    booking =  db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        return None
    
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return booking