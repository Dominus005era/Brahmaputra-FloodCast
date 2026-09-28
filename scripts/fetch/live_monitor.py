import os
import sys
import time
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.fetch.live_service import FloodSenseLiveService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger('FloodSenseMonitor')


def run_continuous_monitor(
    interval_seconds: int = 60,
    output_file: Optional[str] = 'data/live_alert.json',
    max_cycles: Optional[int] = None
):
    service = FloodSenseLiveService()
    output_path = Path(output_file) if output_file else None
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    last_seen_timestamp = None
    last_seen_level = None
    cycle = 0

    logger.info('=' * 75)
    logger.info('FLOODSENSE CONTINUOUS REAL-TIME MONITOR INITIALIZED')
    logger.info('Station: ' + service.STATION_NAME + ' (' + service.DISTRICT + ', ' + service.STATE + ')')
    logger.info('Polling Interval: ' + str(interval_seconds) + ' seconds | Output Target: ' + str(output_file))
    logger.info('=' * 75)

    try:
        while True:
            cycle += 1
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info('[CYCLE #' + str(cycle) + ' - ' + now_str + '] Checking telemetry source...')

            try:
                result = service.get_live_prediction()
                current_ts = result['timestamp']
                current_wl = result['current_water_level']
                source = result.get('data_source', 'UNKNOWN')
                mode = result.get('data_mode', 'UNKNOWN')

                if current_ts != last_seen_timestamp or current_wl != last_seen_level:
                    logger.info('🔔 [NEW TELEMETRY EVENT DETECTED]')
                    logger.info('   Timestamp        : ' + str(current_ts))
                    logger.info('   Data Source      : ' + str(source) + ' (' + str(mode) + ')')
                    logger.info('   Water Level      : ' + str(current_wl) + ' m')
                    logger.info('   Prediction Class : ' + str(result['prediction']) + ' (' + str(result['prediction_label']) + ')')
                    logger.info('   Flood Probability: ' + str(result['probability']))
                    logger.info('   Risk Level       : ' + str(result['risk_level']))
                    logger.info('   Escalation Level : ' + str(result['escalation_level']))

                    if output_path:
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(result, f, indent=2)
                        logger.info('   Alert State Published to: ' + str(output_path))

                    last_seen_timestamp = current_ts
                    last_seen_level = current_wl

                else:
                    logger.info('⏳ [SOURCE UNCHANGED] Timestamp ' + str(current_ts) + ' already processed.')
                    logger.info('   [ACTION] SKIPPED duplicate prediction. System in standby.')

            except Exception as e:
                logger.error('Error during monitor cycle #' + str(cycle) + ': ' + str(e))

            if max_cycles is not None and cycle >= max_cycles:
                logger.info('Reached requested test cycles limit (' + str(max_cycles) + '). Exiting monitor.')
                break

            logger.info('Sleeping for ' + str(interval_seconds) + ' seconds until next polling cycle...\n')
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        logger.info('\n[MONITOR TERMINATED] Continuous monitor stopped gracefully by user.')


def main():
    parser = argparse.ArgumentParser(
        description='FloodSense Continuous Live Stream Monitor'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=60,
        help='Polling interval in seconds (default: 60)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/live_alert.json',
        help='File path to publish real-time alerts'
    )
    parser.add_argument(
        '--max-cycles',
        type=int,
        default=None,
        help='Optional maximum loop cycles (useful for testing)'
    )

    args = parser.parse_args()
    run_continuous_monitor(
        interval_seconds=args.interval,
        output_file=args.output,
        max_cycles=args.max_cycles
    )


if __name__ == '__main__':
    main()