import sys
import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.fetch.live_service import get_live_flood_prediction, FloodSenseLiveService


def main():
    parser = argparse.ArgumentParser(
        description='FloodSense Live Real-Time Telemetry Predictor (Fakirpara Tangni, Darrang, Assam)'
    )
    parser.add_argument(
        '--save',
        type=str,
        default=None,
        help='Optional path to save JSON output'
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Output compact JSON on a single line'
    )

    args = parser.parse_args()

    prediction_dict = get_live_flood_prediction(as_json=False)

    if args.compact:
        output_str = json.dumps(prediction_dict)
    else:
        output_str = json.dumps(prediction_dict, indent=2)

    print(output_str)

    if args.save:
        save_path = Path(args.save)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(output_str)
        print(f'\n[INFO] Output successfully saved to: {save_path}', file=sys.stderr)


if __name__ == '__main__':
    main()