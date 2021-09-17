from app.main.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Item(Base):
    """ List of items to be ranked """
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # _model_id = Column('model_id', String, ForeignKey('model.id'))
    # _category_id = Column('category_id', Integer, ForeignKey('category.id'))
    model_id = Column(String)
    category_id = Column(Integer)
    guid = Column(String, unique=True)
    name = Column(String)
    '''
    implicit_logs = relationship("Implicit_log", back_populates="item")
    explicit_logs = relationship("Explicit_log", back_populates="item")
    model = relationship("Model", back_populates="items")
    category = relationship("Category", back_populates="items")
    '''
        
    def __repr__(self):
        return "<Item '{}'>".format(self.id)