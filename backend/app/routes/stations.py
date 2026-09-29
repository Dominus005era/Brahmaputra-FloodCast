from fastapi import APIRouter
from backend.app.schemas import StationMetadata

router = APIRouter(prefix="/api/stations", tags=["Stations"])

STATION_INFO = StationMetadata(
    station_name="NH15 Crossing Fakirpara Tangni",
    district="Darrang",
    state="Assam",
    river="Tangni River (Tributary of Brahmaputra)",
    basin="Brahmaputra Basin",
    latitude=26.5083,
    longitude=92.1164,
    warning_level_m=58.0,
    danger_level_m=60.0,
    primary_source="National Water Data Portal (NWDP / NWIC Telemetry)",
    auxiliary_source="Copernicus GloFAS & Open-Meteo Real-Time Stream"
)

@router.get("", response_model=list[StationMetadata])
def get_stations():
    """Returns metadata for all monitored river gauge stations."""
    return [STATION_INFO]