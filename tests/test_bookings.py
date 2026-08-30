import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.database import engine, Base, SessionLocal
from app.models.booking import Booking

@pytest.fixture(scope="function") #Фикстура
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")#Создание нового клиента для каждого сервера
def client():
    with TestClient(app) as client:
        yield client


def test_create_booking_success(client, test_db): #тест на создание брони
    payload = {
        "name": "Мария",
        "phone": "+79951067123",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 3
    }
    
    response = client.post("/booking", json=payload)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "Мария"
    assert data["phone"] == "79951067123"
    assert data["booking_date"] == "2026-09-01"
    assert data["booking_time"] == "14:00:00"
    assert data["guests"] == 3
    assert data["status"] == "active"
    assert "id" in data


def test_create_booking_conflict(client, test_db): #тест на создание брони на занятый слот
    payload = {
        "name": "Анна",
        "phone": "79161234567",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 4
    }

    client.post("/booking/", json=payload)
    payload2 = {
        "name": "Пётр",
        "phone": "+79261234567",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 2
    }

    response = client.post("/booking", json=payload2)
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Этот слот занят"


def test_get_bookings_with_data(client, test_db): #Тест на получение списка броней
    payload = {
        "name": "Владимир",
        "phone": "+79939539377",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 1
    }

    client.post("/booking", json=payload)
    response = client.get("/booking")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Владимир"


def test_get_booking_success(client, test_db): #Получение брони по айди
    payload = {
        "name": "Кристина",
        "phone": "+79161234567",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 7
    }

    create_response = client.post("/booking", json=payload)
    booking_id = create_response.json()["id"]
    
    response = client.get(f"/booking/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == booking_id
    assert data["name"] == "Кристина"


def test_get_booking_not_found(client, test_db): #Тест на несуществующую бронь
    response = client.get("/booking/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"


def test_cancel_booking_success(client, test_db): #Тест на отмену брони
    payload = {
        "name": "Анна",
        "phone": "+79161234567",
        "booking_date": "2026-09-01",
        "booking_time": "14:00:00",
        "guests": 4
    }

    create_response = client.post("/booking", json=payload)
    booking_id = create_response.json()["id"]
    
    response = client.delete(f"/booking/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"


def test_cancel_booking_not_found(client, test_db): #Тест на отмену несуществующей брони
    response = client.delete("/booking/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Booking not found"