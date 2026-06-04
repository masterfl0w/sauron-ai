# --- Build Stage (Frontend) ---
FROM node:20-slim AS build-stage
WORKDIR /app/interface
COPY interface/package*.json ./
RUN npm install
COPY interface/ ./
RUN npm run build

# --- Final Stage (Backend + Frontend Assets) ---
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies for psutil and GPUtil (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/api.py ./backend/
RUN pip install fastapi uvicorn psutil gputil requests

# Copy interface build from build-stage
COPY --from=build-stage /app/interface/dist ./interface/dist

# Copy SDK for the orchestrator (if you want to run sauron.py inside, though less likely)
COPY sdk/ ./sdk/
COPY sauron.py ./

# Expose the single port serving both UI and API
EXPOSE 8000

# Run the backend (which now serves the interface dist)
CMD ["python", "backend/api.py"]
