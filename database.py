from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base


DB_URL = "mysql+pymysql://root:Atul%402006@localhost/railway"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

