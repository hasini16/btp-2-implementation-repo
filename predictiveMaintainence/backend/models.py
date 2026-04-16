from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class SensorFeed(Base):
    __tablename__ = "sensor_feeds"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    accel_x = Column(Float, nullable=False)
    accel_y = Column(Float, nullable=False)
    accel_z = Column(Float, nullable=False)
    machine_id = Column(String, default="cnc1", nullable=False)

    def __repr__(self):
        return f"SensorFeed(id={self.id}, accel_x={self.accel_x}, ts={self.timestamp})"
