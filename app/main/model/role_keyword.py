from app.main.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

class Role_keyword(Base):
    "Role keywords for content based recommendations"
    __tablename__ = "role_keyword"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String)
    # _role_id = Column('role_id', Integer, ForeignKey('role.id'))
    role_id = Column(Integer)
    weight = Column(Integer)
    '''
    role = relationship("Role", back_populates="role_keywords")
    '''

    def __repr__(self):
        return "<Role_keyword {} >".format(self.id)