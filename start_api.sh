#!/bin/bash
echo "Starting Todo API Server..."
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""
echo "Starting server..."
echo "API will be available at: http://localhost:8000"
echo "API Docs at: http://localhost:8000/docs"
echo ""
uvicorn api.main:app --reload
