import os
import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8000))
    print('=' * 75)
    print('STARTING FLOODSENSE FASTAPI SERVER')
    print(f'Listening on: http://{host}:{port}')
    print(f'Access Swagger UI at: http://{host}:{port}/docs')
    print(f'Access Health Check at: http://{host}:{port}/health')
    print('=' * 75)
    uvicorn.run('backend.app.main:app', host=host, port=port, reload=False)