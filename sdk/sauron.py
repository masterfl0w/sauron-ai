import requests
import json
import time

class Sauron:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.log_url = f"{backend_url}/log"

    def log(self, step, loss, val_loss=None, lr=None, **kwargs):
        payload = {
            "step": step,
            "loss": loss,
            "val_loss": val_loss,
            "lr": lr,
            "timestamp": time.time(),
            **kwargs
        }
        try:
            response = requests.post(self.log_url, json=payload, timeout=0.5)
            return response.status_code == 200
        except Exception:
            # Silently fail if backend is not reachable to avoid interrupting training
            return False

# Singleton instance
_instance = Sauron()

def log(step, loss, val_loss=None, lr=None, **kwargs):
    return _instance.log(step, loss, val_loss, lr, **kwargs)

def init(backend_url="http://127.0.0.1:8000"):
    global _instance
    _instance = Sauron(backend_url)
