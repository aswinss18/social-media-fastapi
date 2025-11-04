
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

SQLALCHEMY_DATABASE_URL='postgresql://postgres:4166@localhost/social-media-fastapi'

engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base=declarative_base()



# while True:
#     try:
#        conn =psycopg2.connect(host='localhost',database='social-media-fastapi',user='postgres',password='4166',cursor_factory=RealDictCursor)
#        cursor = conn.cursor()
#        print("🟢 🟢 🟢 Database connection was successful! 🟢 🟢 🟢")
#        break
#     except Exception as error:
#        print("🔴 🔴 🔴 Database connection was failed! 🔴 🔴 🔴")
#        print("Error:",error)
#        time.sleep(3)