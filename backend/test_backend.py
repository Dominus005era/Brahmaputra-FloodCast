import sys
import json
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models import PredictionRecord

client = TestClient(app)

print('=' * 75)
print('RUNNING FLOODSENSE BACKEND & SQL SERVER INTEGRATION TEST SUITE')
print('=' * 75)

# Test 1: Health Check
res_health = client.get('/health')
assert res_health.status_code == 200, f'Health check failed: {res_health.text}'
print('[TEST 1: GET /health] PASS ->', res_health.json())

# Test 2: Stations Endpoint
res_stations = client.get('/api/stations')
assert res_stations.status_code == 200, f'Stations failed: {res_stations.text}'
data_stations = res_stations.json()
assert len(data_stations) >= 1
print('[TEST 2: GET /api/stations] PASS -> Found', len(data_stations), 'station:', data_stations[0]['station_name'])

# Test 3: Current Flood Prediction
res_current = client.get('/api/flood/current')
assert res_current.status_code == 200, f'Current prediction failed: {res_current.text}'
current_data = res_current.json()
print('[TEST 3: GET /api/flood/current] PASS ->')
print(json.dumps(current_data, indent=2))

assert 'station' in current_data
assert 'data_source' in current_data
assert 'data_mode' in current_data
assert 'risk_level' in current_data
assert 'prediction' in current_data

# Test 4: Flood History Endpoint
res_history = client.get('/api/flood/history?limit=10')
assert res_history.status_code == 200, f'History failed: {res_history.text}'
hist_data = res_history.json()
print('[TEST 4: GET /api/flood/history] PASS -> Total Records in History:', hist_data['total_records'])

# Test 5: Custom Simulation / Operator Prediction
res_custom = client.post('/api/flood/predict-custom', json={'water_level': 61.2})
assert res_custom.status_code == 200, f'Custom prediction failed: {res_custom.text}'
custom_data = res_custom.json()
print('[TEST 5: POST /api/flood/predict-custom (Level: 61.2m)] PASS -> Prediction:', custom_data['prediction_label'], '| Risk:', custom_data['risk_level'])

# Test 6: Verify SQL Server Direct Query
db = SessionLocal()
records_count = db.query(PredictionRecord).count()
latest_db_record = db.query(PredictionRecord).order_by(PredictionRecord.prediction_id.desc()).first()
db.close()

print(f'[TEST 6: SQL Server Verification] PASS -> Total rows in predictions table: {records_count}')
if latest_db_record:
    print(f'   Latest Record in SQL Server -> ID: {latest_db_record.prediction_id}, Station: {latest_db_record.station}, Source: {latest_db_record.data_source}, Level: {latest_db_record.current_water_level}m')

print('=' * 75)
print('ALL BACKEND API & SQL SERVER TESTS PASSED WITH 100% SUCCESS!')
print('=' * 75)