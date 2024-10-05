from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class NasaModelData(Base):
    __tablename__ = 'nasa_model_data'

    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    model = Column(String, nullable=False)
    csv = Column(String, nullable=False)
    param = Column(String, nullable=False)