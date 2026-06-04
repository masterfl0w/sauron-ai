# Sauron AI Training Monitor

Sauron is a real-time developer dashboard for monitoring AI model training. It provides deep analysis of training metrics and system hardware utilization.

## Structure
- `backend/`: FastAPI server that receives logs and monitors hardware.
- `sdk/`: Simple Python library to integrate into your training scripts.
- `interface/`: React + Vite + Tailwind dashboard.
- `examples/`: Dummy training script to test the integration.

## Installation

### 1. Backend Dependencies
```bash
pip install fastapi uvicorn psutil gputil requests
```

### 2. Frontend Dependencies
```bash
cd interface
npm install
```

## How to run

### Option 1: Using the Sauron CLI (Local)
Everything is managed through the central CLI. It will automatically start the backend, the interface, and verify their status before opening the navigator.

```bash
python sauron.py
```

### Option 2: Using Docker
You can run the entire Sauron service (Dashboard + Backend) in a single container.

```bash
docker-compose up --build
```

1.  **Open the dashboard**: Once initialized, open your browser at `http://localhost:8000`.
2.  **Monitor**: The container will listen for logs on port 8000 and serve the UI on the same port.

*Note: For GPU monitoring inside Docker, ensure you have the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) installed.*

## SDK Usage
```python
import sauron

# In your training loop
sauron.log(
    step=epoch, 
    loss=train_loss, 
    val_loss=val_loss, 
    lr=learning_rate
)
```
