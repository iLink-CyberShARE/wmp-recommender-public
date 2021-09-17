from app.main.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Item_keyword(Base):
    "Item keywords for content based recommendations"
    __tablename__ = "item_keyword"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String)
    # _item_id = Column('item_id', Integer, ForeignKey('item.id'))
    item_id = Column(Integer)
    weight = Column(Integer)
    '''
    item = relationship("Item", back_populates="item_keywords")
    '''

    def __repr__(self):
        return "<Item_keyword {} >".format(self.id)