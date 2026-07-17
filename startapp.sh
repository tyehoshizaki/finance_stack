#!/bin/bash

# Start backend
echo "Starting backend..."

cd backend || exit 1

source .venv/bin/activate

uvicorn app.main:app \
  --reload \
  --host 0.0.0.0 \
  --port 8000 &

BACKEND_PID=$!

# Go back to the project root
cd ..

# Start frontend
echo "Starting frontend..."

cd frontend || exit 1

npm run dev

# When frontend stops, stop backend too
kill $BACKEND_PID