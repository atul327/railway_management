from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator, EmailStr
from datetime import date
from passlib.context import CryptContext
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
# class RegisterSchema(BaseModel):
#     email : EmailStr
#     password : str = Field(min_length=6, max_length=18)
#     conf_pass : str 

#     @model_validator(mode="after")
#     def check_passwords(self):
#         if self.password != self.conf_pass:
#             raise ValueError("Passwords do not match")
#         return self 
    
class PassengerSchema(BaseModel):
    name : str 
    gender : str 
    mobile_no : str 
    email : EmailStr

    @field_validator("mobile_no")
    def check_mobile_no(cls, values):
        if len(values) != 10:
            raise ValueError("Mobile no must have 10 digits")
        elif not values.isdigit():
            raise ValueError("Mobile must contain only numbers")
        
        return values
    
class TrainSchema(BaseModel):
    train_no : int
    train_name : str = Field(min_length=3)


"""Reservation schema ki kuch jada jrurt nhi hai kyo ki o manually and fixed data hi store krega"""
class ReservationSchema(BaseModel):
    reservation_id : int 
    class_type : str = Field(min_length=2)


class TicketSchema(BaseModel):
    journey_date: date
    booking_date: date
    seat_no: int = Field(gt=0)
    passenger_id: int
    train_no: int
    reservation_id: int

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# @app.post("/register")
# def register(user : RegisterSchema, db : Session = Depends(get_db)):
    
#     # db = SessionLocal()
    
#     check_email = db.query(models.User).filter(models.User.email == user.email).first()

#     if check_email:
#         raise ValueError(status_code = 400, detail = "Email already exists")
    
#     hashed = hash_password(user.password)
    
#     new_user = models.User(
#         email = user.email,
#         password = hashed
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message" : "User Register Successfully"}

@app.post('/passenger')
def passenger_details(passenger : PassengerSchema, db : Session = Depends(get_db)):

    # db = SessionLocal()
    check_passenger = db.query(models.Passenger).filter(models.Passenger.email == passenger.email).first()

    if check_passenger:
        raise HTTPException(status_code=401, detail="Passenger already exists")

    new_passenger = models.Passenger(
        name = passenger.name,
        gender = passenger.gender,
        mobile_no = passenger.mobile_no,
        email = passenger.email
    )

    db.add(new_passenger)
    db.commit()
    db.refresh(new_passenger)

    return {"message" : "Passenger added"}

@app.get('/view_passenger')
def view_passenger(db : Session = Depends(get_db)):

    # db = SessionLocal()

    return db.query(models.Passenger).all()


@app.post('/add_train')
def add_train(train : TrainSchema, db : Session = Depends(get_db)):
    new_train = models.Train(
        train_no = train.train_no,
        train_name = train.train_name
    )

    db.add(new_train)
    db.commit()
    db.refresh(new_train)

    return {"message" : "New Train added"}

@app.get("/view_train")
def view_train(db: Session = Depends(get_db)):
    return db.query(models.Train).all()

@app.post("/add_reservation")
def add_reservation(reservation: ReservationSchema, db: Session = Depends(get_db)):

    new_res = models.Reservation(
        reservation_id=reservation.reservation_id,
        class_type=reservation.class_type
    )

    db.add(new_res)
    db.commit()
    db.refresh(new_res)

    return {"message": "Reservation added"}

@app.get("/view_reservations")
def view_reservations(db: Session = Depends(get_db)):
    return db.query(models.Reservation).all()

@app.post('/add_ticket')
def add_ticket(ticket : TicketSchema, db : Session = Depends(get_db)):

    passenger = db.query(models.Passenger).filter(models.Passenger.passenger_id == ticket.passenger_id).first()

    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    train = db.query(models.Train).filter(models.Train.train_no == ticket.train_no).first()

    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    
    exist = db.query(models.Ticket).filter(
        models.Ticket.train_no == ticket.train_no,
        models.Ticket.journey_date == ticket.journey_date,
        models.Ticket.seat_no == ticket.seat_no
    ).first()

    if exist:
        raise HTTPException(status_code=400, detail = "Seat already booked for this train on this date")
    
    new_ticket = models.Ticket(
        journey_date = ticket.journey_date,
        booking_date = ticket.booking_date,
        seat_no = ticket.seat_no,
        passenger_id = ticket.passenger_id,
        train_no = ticket.train_no,
        reservation_id = ticket.reservation_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {"message" : "Ticket Booked Successfully"}

@app.get("/view_tickets")
def view_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)