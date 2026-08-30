import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.bookings import router as bookings_router
from app.core.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI(title = "Booking API", lifespan=lifespan)
app.include_router(bookings_router, prefix="/booking", tags=["Bookings"])

@app.get("/")
def root():
    return{"message": "Booking API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload = True)