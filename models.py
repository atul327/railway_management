from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from database import Base, engine

# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     email = Column(String, unique=True, nullable=False)
#     password = Column(String)

class Passenger(Base):
    __tablename__ = "passenger"

    passenger_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    gender = Column(String)
    mobile_no = Column(String)
    email = Column(String)

class Train(Base):
    __tablename__ = "train"

    train_no = Column(Integer, primary_key=True)
    train_name = Column(String)

class Reservation(Base):
    __tablename__ = "reservation"

    reservation_id = Column(Integer, primary_key=True)
    class_type = Column(String, nullable=False)

class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    journey_date = Column(Date)
    booking_date = Column(Date)
    seat_no = Column(Integer)
    passenger_id = Column(Integer, ForeignKey("passenger.passenger_id"))
    train_no = Column(Integer, ForeignKey("train.train_no"))
    reservation_id = Column(Integer, ForeignKey("reservation.reservation_id"))

# Base.metadata.create_all(bind = engine)