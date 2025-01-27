from sqlalchemy import  Integer, String , JSON
from sqlalchemy.orm import Mapped, mapped_column , relationship
from database import Base

class Farmer(Base):
    __tablename__ = "farmers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    crops: Mapped[list[str]] = mapped_column(JSON)


    diseased_crops = relationship("DiseasePredictor", back_populates="farmer", cascade="all, delete-orphan" , passive_deletes=True)
    factors = relationship("Factors", back_populates="farmer", cascade="all, delete-orphan", passive_deletes=True , )