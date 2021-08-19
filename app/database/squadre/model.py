from app.database import Base
from sqlalchemy import Column,Integer, String
from random import randint
class Squadre(Base):
    __tablename__ = "squadre"
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    code= Column(String(5),nullable=False,default= ''.join(["{}".format(randint(0, 9)) for num in range(0, 5)]))