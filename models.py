from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    rarity = Column(String(25))
    season = Column(String(6))
    item_type = Column(String(35))
    name = Column(String(150))

    def __repr__(self):
        return f"ID: {self.id}\nRARITY: {self.rarity}\nSEASON: {self.season}\nITEM: {self.item_type}\nNAME: {self.name}"