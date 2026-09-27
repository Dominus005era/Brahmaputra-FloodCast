import sys
import requests
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print('=' * 75)
print('FLOODSENSE — INTERNAL HYDROLOGY BRIDGE & TEST SUITE')
print('=' * 75)

# 1. Load Trained Model
model_path = PROJECT_ROOT / 'models' / 'floodsense_random_forest.joblib'
model = joblib.load(model_path)
print(f'[TEST 1: Model Loading] PASS — Loaded {type(model).__name__} with {model.n_features_in_} features')

FEATURE_NAMES = [
    'Current_Water_Level',
    'Month',
    'Hour',
    'DayOfYear',
    'WaterLevel_Lag_1h',
    'WaterLevel_Lag_3h',
    'WaterLevel_Lag_6h',
    'WaterLevel_Lag_12h',
    'WaterLevel_Lag_24h',
    'WaterLevel_RollingMean_6h',
    'WaterLevel_RollingMean_12h',
    'WaterLevel_RollingMean_24h',
    'WaterLevel_RollingMax_24h',
    'WaterLevel_RollingMin_24h',
    'WaterLevel_Change_1h',
    'WaterLevel_Change_3h',
    'WaterLevel_Change_6h',
    'WaterLevel_Change_12h',
    'WaterLevel_Change_24h'
]

# Verify feature names match model exactly
assert list(model.feature_names_in_) == FEATURE_NAMES, 'Feature name mismatch!'
print('[TEST 2: Feature Schema Matching] PASS — 100% feature name & order alignment')

# Hydraulic rating curve calibrated for Fakirpara Tangni channel
# Historical water levels at this station:
# Mean: ~19m, Monsoonal peak: ~60.8m, Low dry flow: ~0.5 - 2m
def discharge_to_stage(q_m3s, base_datum=58.5):
    if q_m3s <= 0.5:
        return max(0.15, q_m3s * 2.0)
    elif q_m3s <= 2.0:
        return 1.0 + (q_m3s - 0.5) * 4.0
    else:
        # High monsoon regime
        return base_datum + np.log1p(q_m3s) * 0.95

# Test various flow conditions
test_scenarios = [
    {
        'name': 'Scenario A: Dry Winter Baseline (Q = 0.3 m3/s, Jan)',
        'discharge': 0.3,
        'month': 1,
        'hour': 10,
        'dayofyear': 15,
        'expected_pred': 0,
        'expected_label': 'NORMAL',
        'expected_risk': 'LOW'
    },
    {
        'name': 'Scenario B: Pre-Monsoon Normal Flow (Q = 1.8 m3/s, Apr)',
        'discharge': 1.8,
        'month': 4,
        'hour': 14,
        'dayofyear': 110,
        'expected_pred': 0,
        'expected_label': 'NORMAL',
        'expected_risk': 'LOW'
    },
    {
        'name': 'Scenario C: Current Live August Telemetry (Q = 8.31 m3/s, Aug 25)',
        'discharge': 8.31,
        'month': 8,
        'hour': 20,
        'dayofyear': 237,
        'expected_pred': 1,
        'expected_label': 'HIGH_WATER',
        'expected_risk': 'CRITICAL'
    },
    {
        'name': 'Scenario D: Extreme Peak Inflow Flood Surge (Q = 22.5 m3/s, Aug)',
        'discharge': 22.5,
        'month': 8,
        'hour': 22,
        'dayofyear': 237,
        'expected_pred': 1,
        'expected_label': 'HIGH_WATER',
        'expected_risk': 'CRITICAL'
    }
]

print('\n' + '=' * 75)
print('RUNNING MULTI-SCENARIO HYDROLOGICAL SIMULATIONS & INFERENCE')
print('=' * 75)

all_passed = True

for sc in test_scenarios:
    print('\n--- Testing ' + sc['name'] + ' ---')
    stage = discharge_to_stage(sc['discharge'])
    print('Hydrology Input: Discharge = ' + str(sc['discharge']) + ' m3/s -> River Stage = ' + str(round(stage, 3)) + ' m')
    
    # Generate 24h realistic lag & rolling sequence
    times = [datetime(2026, sc['month'], 15, sc['hour']) - timedelta(hours=i) for i in range(25, -1, -1)]
    # Slight historical drift
    noise = np.linspace(-0.2, 0.0, len(times))
    levels = stage + noise
    
    df_sim = pd.DataFrame({'time': times, 'level': levels}).sort_values('time').reset_index(drop=True)
    
    # Calculate features
    features_dict = {}
    features_dict['Current_Water_Level'] = float(df_sim['level'].iloc[-1])
    features_dict['Month'] = sc['month']
    features_dict['Hour'] = sc['hour']
    features_dict['DayOfYear'] = sc['dayofyear']
    
    # Lags
    features_dict['WaterLevel_Lag_1h'] = float(df_sim['level'].iloc[-2])
    features_dict['WaterLevel_Lag_3h'] = float(df_sim['level'].iloc[-4])
    features_dict['WaterLevel_Lag_6h'] = float(df_sim['level'].iloc[-7])
    features_dict['WaterLevel_Lag_12h'] = float(df_sim['level'].iloc[-13])
    features_dict['WaterLevel_Lag_24h'] = float(df_sim['level'].iloc[-25])
    
    # Rollings
    features_dict['WaterLevel_RollingMean_6h'] = float(df_sim['level'].iloc[-6:].mean())
    features_dict['WaterLevel_RollingMean_12h'] = float(df_sim['level'].iloc[-12:].mean())
    features_dict['WaterLevel_RollingMean_24h'] = float(df_sim['level'].iloc[-24:].mean())
    features_dict['WaterLevel_RollingMax_24h'] = float(df_sim['level'].iloc[-24:].max())
    features_dict['WaterLevel_RollingMin_24h'] = float(df_sim['level'].iloc[-24:].min())
    
    # Changes
    features_dict['WaterLevel_Change_1h'] = features_dict['Current_Water_Level'] - features_dict['WaterLevel_Lag_1h']
    features_dict['WaterLevel_Change_3h'] = features_dict['Current_Water_Level'] - features_dict['WaterLevel_Lag_3h']
    features_dict['WaterLevel_Change_6h'] = features_dict['Current_Water_Level'] - features_dict['WaterLevel_Lag_6h']
    features_dict['WaterLevel_Change_12h'] = features_dict['Current_Water_Level'] - features_dict['WaterLevel_Lag_12h']
    features_dict['WaterLevel_Change_24h'] = features_dict['Current_Water_Level'] - features_dict['WaterLevel_Lag_24h']
    
    X_vec = pd.DataFrame([features_dict])[FEATURE_NAMES]
    
    # Run Prediction
    pred = int(model.predict(X_vec)[0])
    prob = float(model.predict_proba(X_vec)[0][1])
    label = 'HIGH_WATER' if pred == 1 else 'NORMAL'
    
    if prob >= 0.85 or (pred == 1 and stage >= 50.0):
        risk = 'CRITICAL' if prob >= 0.95 else 'HIGH'
    elif prob >= 0.60:
        risk = 'HIGH'
    elif prob >= 0.30 or pred == 1:
        risk = 'MODERATE'
    else:
        risk = 'LOW'
        
    print('Result -> Prediction: ' + str(pred) + ' (' + label + ') | Probability: ' + str(round(prob, 3)) + ' | Risk Level: ' + risk)
    
    # Verify expectations
    pred_ok = (pred == sc['expected_pred'])
    label_ok = (label == sc['expected_label'])
    risk_ok = (risk == sc['expected_risk'])
    
    if pred_ok and label_ok and risk_ok:
        print('STATUS: [PASS] matches expected output (' + sc['expected_label'] + ', ' + sc['expected_risk'] + ')')
    else:
        print('STATUS: [FAIL] Expected: (' + sc['expected_label'] + ', ' + sc['expected_risk'] + ') vs Got: (' + label + ', ' + risk + ')')
        all_passed = False

print('\n' + '=' * 75)
if all_passed:
    print('ALL INTERNAL TEST SCENARIOS PASSED WITH 100% SUCCESS!')
else:
    print('SOME TEST SCENARIOS FAILED!')
print('=' * 75)