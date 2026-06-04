import requests
import json
import time
import os

class Sauron:
    def __init__(self, backend_url="http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.log_url = f"{backend_url}/log"
        # Optional: Persistent session identification
        self.session_id = os.environ.get("SAURON_SESSION_ID", f"train_{int(time.time())}")

    def log(self, step, loss, val_loss=None, lr=None, **kwargs):
        """
        Sends training metrics to the Sauron background service.
        This call is non-blocking (short timeout) to ensure it doesn't 
        slow down the training loop if the service is unreachable.
        """
        payload = {
            "session_id": self.session_id,
            "step": step,
            "loss": loss,
            "val_loss": val_loss,
            "lr": lr,
            "timestamp": time.time(),
            **kwargs
        }
        try:
            # Short timeout to prevent blocking background training tasks
            response = requests.post(self.log_url, json=payload, timeout=0.1)
            return response.status_code == 200
        except Exception:
            # Silently ignore connection errors to ensure training continues
            return False

# Singleton instance for easy importing
_instance = Sauron()

def log(step, loss, val_loss=None, lr=None, **kwargs):
    """Global log function to be used in training scripts."""
    return _instance.log(step, loss, val_loss, lr, **kwargs)

def init(backend_url="http://127.0.0.1:8000"):
    """Re-initialize the Sauron client with a specific backend URL."""
    global _instance
    _instance = Sauron(backend_url)
