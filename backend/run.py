import uvicorn
import sys
import os

# Backend klasöründen çalıştırıldığında path'i ayarla
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 