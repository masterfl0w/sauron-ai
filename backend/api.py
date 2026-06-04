from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import json
import psutil
import os
import subprocess
import platform
import re

try:
    import GPUtil
except ImportError:
    GPUtil = None

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in clients:
            clients.remove(websocket)
    except Exception:
        if websocket in clients:
            clients.remove(websocket)

async def broadcast(message: dict):
    if not clients:
        return
    disconnected = set()
    for client in list(clients):
        try:
            await client.send_json(message)
        except Exception:
            disconnected.add(client)
    for client in disconnected:
        if client in clients:
            clients.remove(client)

@app.post("/log")
async def log_metrics(metrics: dict):
    await broadcast({"type": "training_metrics", "data": metrics})
    return {"status": "ok"}

def get_apple_silicon_stats():
    """
    Attempts to get Apple Silicon GPU stats using 'ioreg'.
    This is more reliable than 'powermetrics' which requires sudo.
    """
    try:
        # Get GPU utilization
        cmd = ["ioreg", "-n", "AGXAccelerator", "-r", "-l"]
        output = subprocess.check_output(cmd).decode("utf-8")
        
        # Look for "performance statistics" which contains utilization
        # Note: This regex is specifically for Apple Silicon AGX
        util_match = re.search(r'"performance statistics" = {.*"Device Utilization %"=(\d+)', output, re.DOTALL)
        gpu_load = float(util_match.group(1)) if util_match else 0.0
        
        # Get chip name for display
        chip_cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
        chip_name = subprocess.check_output(chip_cmd).decode("utf-8").strip()
        
        return [{
            "id": 0,
            "name": chip_name,
            "load": gpu_load,
            "memory_util": 0, # M-series uses Unified Memory, already covered by system RAM
            "temp": 0, # Temp is harder to get without sudo
            "type": "apple"
        }]
    except Exception:
        return []

async def hardware_monitor():
    is_mac = platform.system() == "Darwin"
    is_arm = platform.machine() == "arm64"
    
    while True:
        cpu_usage = psutil.cpu_percent(interval=None) # Use None to avoid blocking
        ram_usage = psutil.virtual_memory().percent
        
        gpu_info = []
        
        # 1. Try NVIDIA (GPUtil)
        if GPUtil:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    gpu_info.append({
                        "id": gpu.id,
                        "name": gpu.name,
                        "load": float(gpu.load) * 100,
                        "memory_util": float(gpu.memoryUtil) * 100,
                        "temp": float(gpu.temperature),
                        "type": "nvidia"
                    })
            except Exception:
                pass

        # 2. Try Apple Silicon if on Mac ARM and no NVIDIA found
        if not gpu_info and is_mac and is_arm:
            gpu_info = get_apple_silicon_stats()

        await broadcast({
            "type": "hardware_stats",
            "data": {
                "cpu": cpu_usage,
                "ram": ram_usage,
                "gpu": gpu_info
            }
        })
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(hardware_monitor())

interface_dist = os.path.join(os.path.dirname(__file__), "..", "interface", "dist")
if os.path.exists(interface_dist):
    assets_dir = os.path.join(interface_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    @app.get("/")
    async def get_index():
        return FileResponse(os.path.join(interface_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
