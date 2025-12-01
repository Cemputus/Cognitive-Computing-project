# Backend API

## Starting the Server

**Important**: Always run from the project root, not from `src/api`:

```powershell
# From project root (D:\Cognitive Computing)
cd src\api
python backend_api.py
```

Or use the provided scripts from the project root:
```powershell
# From project root
.\start_backend.bat
```

## Path Configuration

The backend automatically detects the project root and adds it to the Python path, so imports work correctly regardless of where you run it from.

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'src'`:
1. Make sure you're running from the project root or using the start scripts
2. The path detection should work automatically, but if issues persist, check that the project structure is correct

## Dependencies

Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

Key backend dependencies:
- flask
- flask-cors
- PyJWT
- pandas
- numpy

