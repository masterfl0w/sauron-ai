# Sauron AI Training Monitor

Sauron is a professional real-time developer dashboard for monitoring AI model training.

## 🚀 Quick Start (Local Setup)

1. **Install Backend Dependencies**
   ```bash
   pip install fastapi uvicorn psutil gputil requests websockets
   ```

2. **Initialize Background Service**
   This sets up Sauron as a persistent macOS service on your Mac mini.
   ```bash
   ./setup_sauron_service.sh
   ```

3. **Open Dashboard**
   Visit `http://127.0.0.1:8000` in your browser.

---

## 📦 How to use Sauron in ANY project

To use Sauron in a different repository or project, you just need to install the SDK.

### 1. Install the SDK Globally
In your terminal, navigate to the `sdk/` folder of this repository and run:
```bash
cd sdk
pip install -e .
```
*Note: Using `-e` (editable mode) is recommended so any updates to Sauron are immediately available to your scripts.*

### 2. Add to your Training Script
In any Python file across your computer, you can now import and use the monitor:

```python
import sauron_monitor as sauron

# In your training loop
sauron.log(
    step=epoch, 
    loss=train_loss, 
    val_loss=val_loss, 
    lr=optimizer.param_groups[0]['lr']
)
```

### 3. Connection Config
The SDK defaults to `127.0.0.1:8000`. If your background service is running on a different port or machine, initialize it once at the top of your script:
```python
sauron.init("http://10.0.1.5:8000") # Replace with your Mac mini IP if remote
```

---

## 👁️ Interactive Shell (Sauron CLI)
For manual navigation and launching scripts from this folder:
```bash
python sauron.py
```
- `ls`, `cd`, `pwd`: Standard navigation.
- `run <script.py>`: Launch a script with Sauron monitoring.
- `status`: Check if the background service is alive.

## 🐳 Docker
```bash
docker-compose up --build
```
Access dashboard at `http://localhost:8000`.
