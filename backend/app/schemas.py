from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class FloodPredictionResponse(BaseModel):
    station: str = Field(..., description="Station name")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    data_source: str = Field(..., description="Data source: NWDP or HYDROLOGY_BRIDGE")
    data_mode: str = Field(..., description="Data mode: GROUND_TELEMETRY or DERIVED_HYDROLOGY")
    timestamp: str = Field(..., description="ISO formatted timestamp")
    current_water_level: Optional[float] = Field(None, description="River water level in meters")
    prediction: Optional[int] = Field(None, description="Prediction class: 0 (Normal) or 1 (High Water)")
    prediction_label: str = Field(..., description="Prediction label: NORMAL or HIGH_WATER")
    probability: float = Field(..., description="Flood probability [0.0 - 1.0]")
    risk_level: str = Field(..., description="Risk level: LOW, MODERATE, HIGH, CRITICAL")
    escalation_level: str = Field(..., description="Escalation level: NONE, LOCAL, DISTRICT, STATE")
    status: str = Field(..., description="Telemetry status: ACTIVE or STALE")

    class Config:
        from_attributes = True

class FloodHistoryResponse(BaseModel):
    station: str
    total_records: int
    history: List[FloodPredictionResponse]

class StationMetadata(BaseModel):
    station_name: str
    district: str
    state: str
    river: str
    basin: str
    latitude: float
    longitude: float
    warning_level_m: float
    danger_level_m: float
    primary_source: str
    auxiliary_source: str

class CustomPredictionRequest(BaseModel):
    water_level: float = Field(..., description="Custom gauge level in meters (e.g. 61.2)")