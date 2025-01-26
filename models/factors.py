from sqlalchemy import  Integer, String ,  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship
from database import Base
from datetime import datetime

class Factors(Base):
    __tablename__ = "factors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String, index=True)
    state: Mapped[str] = mapped_column(String, index=True)
    latitude : Mapped[float] = mapped_column(String, index=True)
    longitude : Mapped[float] = mapped_column(String, index=True)
    # month : Mapped[int] = mapped_column(Integer, default=datetime.now().month , index=True) 
    # year : Mapped[int]= mapped_column(Integer, default=datetime.now().year , index=True)
    temperature : Mapped[String] = mapped_column(String, index=True)
    weather : Mapped[str] = mapped_column(String, index=True)
    soil_type : Mapped[str] = mapped_column(String, index=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmers.id", ondelete="CASCADE") , index=True)
    farmer = relationship("Farmer", back_populates="factors" , passive_deletes=True)