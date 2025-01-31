from sqlalchemy import  Integer, String , JSON , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship
from database import Base


class DiseasePredictor(Base):
    __tablename__ = "disease_predictors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True , nullable=True)
    infected_plant_image: Mapped[str] = mapped_column(String, index=True , nullable=True)
    plant_name: Mapped[str] = mapped_column(String, index=True , nullable=True)
    disease_name: Mapped[str] = mapped_column(String, index=True , nullable=True)
    pests : Mapped[str] = mapped_column(String , default="None" , nullable=True)
    symptoms: Mapped[list[str]] = mapped_column(JSON , nullable=True)
    symptom_description: Mapped[str] = mapped_column(String , default="No description available" , nullable=True)
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmers.id", ondelete="CASCADE") , index=True , nullable=True)
    farmer = relationship("Farmer", back_populates="diseased_crops" , passive_deletes=True)

    Cause_of_disease: Mapped[str] = mapped_column(String , default="No solution available" , nullable=True)
    Precautions_to_take: Mapped[str] = mapped_column(String , default="No solution available" , nullable=True)
    Treatment: Mapped[str] = mapped_column(String , default="No solution available" , nullable=True)
    severity: Mapped[str] = mapped_column(String , default="None" , nullable=True)
    time_to_treatment: Mapped[str] = mapped_column(String , default="None" , nullable=True)
    