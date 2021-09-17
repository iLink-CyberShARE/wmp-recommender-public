from app.main.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Category(Base):
    """ Item category groupings """
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    '''
    items = relationship("Item", back_populates="category")
    '''

    def __repr__(self):
        return "<Category '{}'>".format(self.id)