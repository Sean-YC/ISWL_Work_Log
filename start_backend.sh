#!/bin/bash

# 切換到專案目錄
cd "$(dirname "$0")"

# 啟動虛擬環境
echo "✅ Activating virtual environment..."
source venv/bin/activate

# 啟動 FastAPI + uvicorn
echo "🚀 Starting FastAPI server with uvicorn..."
uvicorn app.main:app --reload
