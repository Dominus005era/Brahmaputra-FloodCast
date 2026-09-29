-- FloodSense AI: SQL Server Database Schema
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'FloodSenseDB')
    CREATE DATABASE FloodSenseDB;
GO

USE FloodSenseDB;
GO

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'predictions')
BEGIN
    CREATE TABLE predictions (
        prediction_id BIGINT IDENTITY(1,1) PRIMARY KEY,
        station NVARCHAR(150) NOT NULL,
        district NVARCHAR(100) NOT NULL,
        state NVARCHAR(100) NOT NULL,
        data_source VARCHAR(50) NOT NULL,       -- 'NWDP' | 'HYDROLOGY_BRIDGE' | 'NONE'
        data_mode VARCHAR(50) NOT NULL,         -- 'GROUND_TELEMETRY' | 'DERIVED_HYDROLOGY' | 'UNAVAILABLE'
        timestamp DATETIME2 NOT NULL,
        current_water_level FLOAT NULL,
        prediction INT NULL,                    -- 0 (Normal) | 1 (High Water) | NULL
        prediction_label VARCHAR(50) NOT NULL,  -- 'NORMAL' | 'HIGH_WATER' | 'UNKNOWN'
        probability FLOAT NOT NULL,
        risk_level VARCHAR(50) NOT NULL,        -- 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL' | 'UNKNOWN'
        escalation_level VARCHAR(50) NOT NULL,  -- 'NONE' | 'LOCAL' | 'DISTRICT' | 'STATE'
        status VARCHAR(50) NOT NULL,            -- 'ACTIVE' | 'STALE'
        created_at DATETIME2 DEFAULT SYSUTCDATETIME(),

        CONSTRAINT UQ_station_timestamp_source UNIQUE (station, timestamp, data_source)
    );

    CREATE NONCLUSTERED INDEX IX_predictions_station_time 
    ON predictions (station, timestamp DESC);
END
GO