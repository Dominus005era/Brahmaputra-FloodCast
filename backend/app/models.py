from sqlalchemy import Column, BigInteger, String, Float, Integer, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func
from backend.app.database import Base

class PredictionRecord(Base):
    __tablename__ = "predictions"

    prediction_id = Column(BigInteger, primary_key=True, autoincrement=True)
    station = Column(String(150), nullable=False)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    data_source = Column(String(50), nullable=False)       # 'NWDP' | 'HYDROLOGY_BRIDGE' | 'NONE'
    data_mode = Column(String(50), nullable=False)         # 'GROUND_TELEMETRY' | 'DERIVED_HYDROLOGY' | 'UNAVAILABLE'
    timestamp = Column(DateTime, nullable=False)
    current_water_level = Column(Float, nullable=True)
    prediction = Column(Integer, nullable=True)            # 0 | 1 | None
    prediction_label = Column(String(50), nullable=False)  # 'NORMAL' | 'HIGH_WATER' | 'UNKNOWN'
    probability = Column(Float, nullable=False)
    risk_level = Column(String(50), nullable=False)        # 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL' | 'UNKNOWN'
    escalation_level = Column(String(50), nullable=False)  # 'NONE' | 'LOCAL' | 'DISTRICT' | 'STATE'
    status = Column(String(50), nullable=False)            # 'ACTIVE' | 'STALE'
    created_at = Column(DateTime, default=func.now())

    __table_args__ = (
        UniqueConstraint('station', 'timestamp', 'data_source', name='UQ_station_timestamp_source'),
        Index('IX_predictions_station_time', 'station', 'timestamp')
    )