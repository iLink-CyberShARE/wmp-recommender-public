from app.main.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Role(Base):
    """ Role Model for storing list of available user roles or groups """
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    '''
    implicit_logs = relationship("Implicit_log", back_populates="role")
    explicit_logs = relationship("Explicit_log", back_populates="role")
    role_keywords = relationship("Role_keyword", back_populates="role")
    '''

    def __repr__(self):
        return "<Role '{}'>".format(self.id)