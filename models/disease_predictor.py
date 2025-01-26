from sqlalchemy import  Integer, String , JSON , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column , relationship
from database import Base


class DiseasePredictor(Base):
    __tablename__ = "disease_predictors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    plant_name: Mapped[str] = mapped_column(String, index=True)
    disease_name: Mapped[str] = mapped_column(String, index=True)
    symptoms: Mapped[list[str]] = mapped_column(JSON)
    symptom_description: Mapped[str] = mapped_column(String , default="No description available")
    farmer_id: Mapped[int] = mapped_column(Integer, ForeignKey("farmers.id", ondelete="CASCADE") , index=True)
    farmer = relationship("Farmer", back_populates="diseased_crops" , passive_deletes=True)

    Preventive_measures: Mapped[str] = mapped_column(String , default="No preventive measures available")
    treatment: Mapped[str] = mapped_column(String , default="No treatment available")
    treatment_description: Mapped[str] = mapped_column(String , default="No treatment description available")
    severity: Mapped[str] = mapped_column(String , default="None")
    state: Mapped[str] = mapped_column(String , default="None")
    time_to_treatment: Mapped[str] = mapped_column(String , default="None")
    