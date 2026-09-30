import uvicorn
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if __name__ == '__main__':
    print('=' * 75)
    print('STARTING FLOODSENSE FASTAPI SERVER WITH SQL SERVER BACKEND')
    print('Access Swagger UI at: http://localhost:8000/docs')
    print('Access Health Check at: http://localhost:8000/health')
    print('=' * 75)
    uvicorn.run('backend.app.main:app', host='0.0.0.0', port=8000, reload=False)