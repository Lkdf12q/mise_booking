from datetime import date, time, timedelta
from pydantic import BaseModel, Field, field_validator, ConfigDict
import re

class BookingCreate(BaseModel):#схема для входящих данных
    name: str = Field(min_length= 2, description="Имя гостя")
    phone: str = Field(description="Телефон в формате +7XXXXXXXXXX или 8XXXXXXXXXX")
    booking_date: date = Field(description="Дата бронирования")
    booking_time: time = Field(description="Время бронирования (12:00-22:00, только часы)")
    guests: int = Field(ge=1, le = 12, description="Количество гостей от 1 до 12")

    @field_validator('name')#Валидатор для имени
    @classmethod
    def validate_name(cls, value:str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError('Имя должно содержать минимум 2 символа')
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s-]+$', cleaned):
            raise ValueError('Имя должно содержать только буквы, пробелы и дефис')
        return cleaned

    @field_validator('phone')#Валидатор для телефона
    @classmethod
    def validate_phone(cls, value:str) -> str:
        digits = re.sub(r'\D', '', value)

        if len(digits) == 11 and digits[0] in ('7', '8'):
            return digits
        raise ValueError('Телефон должен быть в формате +7XXXXXXXXXX или 8XXXXXXXXXX')

    @field_validator('booking_date')#Валидатор для даты
    @classmethod
    def validate_date(cls, value:date) -> date:
        today = date.today()

        if value < today:
            raise ValueError('Дата бронирования не может быть раньше сегодняшнего дня')
        
        max_date = today + timedelta(days = 90)
        if value > max_date:
            raise ValueError('Дата бронирования не может быть позднее 90 дней от сегодня')
        return value
    
    @field_validator('booking_time')#Валидатор для времени
    @classmethod
    def validate_time(cls, value:time) -> time:
        if not (12 <= value.hour <= 22):
            raise ValueError('Время должно быть от 12:00 до 22:00')
        if value.minute != 0 or value.second != 0:
            raise ValueError('Время должно быть точным часом (12:00, 13:00 и т.д.)')
        return value
    
class BookingOut(BookingCreate):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)