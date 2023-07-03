from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from mapeamento import *

class DAO():
    def getSession():
        engine = create_engine("postgresql+psycopg2://postgres:fabosmati@192.168.20.224:5432/IGDB") #200.235.88.87
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
