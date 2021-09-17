from app.main.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Model(Base):
    """ List of recommendation models """
    __tablename__ = "model"

    id = Column(String, primary_key=True)
    name = Column(String)
    context_iri = Column(String)
    '''
    items = relationship("Item", back_populates="model")
    trainings = relationship("Training", back_populates="model")
    '''
    def __repr__(self):
        return "<Model '{}'>".format(self.id)
