from app.main.database import Base
from sqlalchemy import Column, Integer, String

class Hush(Base):
    """ Hush table that hold jwt secret keys """
    __tablename__ = "hush"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)

    def __repr__(self):
        return "<Hush '{}'>".format(self.id)