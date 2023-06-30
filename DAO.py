from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from mapeamento import *

class DAO():
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/IGDB")
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
