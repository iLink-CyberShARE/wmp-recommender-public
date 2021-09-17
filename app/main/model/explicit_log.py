from app.main.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

class Explicit_log(Base):
    """ Log for explicit interactions i.e. item rankings from users """
    __tablename__ = "explicit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # _item_id = Column('item_id', Integer, ForeignKey('item.id'))
    item_id = Column(Integer)
    rank_value = Column(Integer)
    user_id = Column(Integer)
    run_id = Column(String)
    # _role_id = Column('role_id', Integer, ForeignKey('role.id'))
    role_id = Column(Integer)
    '''
    item = relationship("Item", back_populates="explicit_logs")
    role = relationship("Role", back_populates="explicit_logs")
    '''
    
    def __repr__(self):
        return "<Explicit_log '{}'>".format(self.id)