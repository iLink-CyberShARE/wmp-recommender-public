from app.main.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

class Implicit_log(Base):
    """ Log for implicit interactions i.e. item views from users """
    __tablename__ = "implicit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # _item_id = Column('item_id', Integer, ForeignKey('item.id'))
    item_id = Column(Integer)
    user_id = Column(Integer)
    run_id = Column(String)
    # _role_id = Column('role_id', Integer, ForeignKey('role.id'))
    role_id = Column(Integer)
    '''
    item = relationship("Item", back_populates="implicit_logs")
    role = relationship("Role", back_populates="implicit_logs")
    '''

    def __repr__(self):
        return "<Implicit_log {} >".format(self.id)