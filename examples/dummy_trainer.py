import sys
import os
import time
import random
import math

import sauron_monitor as sauron

def train():
    print("Starting dummy training...")
    steps = 1000
    lr = 0.001
    
    for step in range(steps):
        # Simulate loss decreasing with some noise
        loss = 2.0 * math.exp(-step / 200) + random.uniform(0, 0.1)
        val_loss = 2.2 * math.exp(-step / 250) + random.uniform(0, 0.15)
        
        # Simulate learning rate decay
        current_lr = lr * (0.99 ** (step // 50))
        
        print(f"Step {step}: loss={loss:.4f}, val_loss={val_loss:.4f}, lr={current_lr:.6f}")
        
        sauron.log(step=step, loss=loss, val_loss=val_loss, lr=current_lr)
        
        time.sleep(0.5)  # Simulate some work

if __name__ == "__main__":
    train()
