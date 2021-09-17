from app.main.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

class Training(Base):
    """ Model training status """
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # _model_id = Column('model_id', String, ForeignKey('model.id'))
    model_id = Column(String)
    status = Column(String)
    message = Column(String)
    last_trained = Column(DateTime)
    num_users = Column(Integer)
    num_items = Column(Integer)
    model_file = Column(String)
    implicit = Column(Boolean)
    explicit = Column(Boolean)
    content = Column(Boolean)
    test_percent = Column(Float)
    learning_rate = Column(Float)
    epochs = Column(Integer)
    loss = Column(String)
    user_alpha = Column(Float)
    item_alpha = Column(Float)
    '''
    model = relationship("Model", back_populates="trainings")
    '''
    
    def __repr__(self):
        return "<Output '{}'>".format(self.id)