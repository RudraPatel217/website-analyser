#!/usr/bin/env bash
# =====================================================
#   Domain Intelligence Agent & SEO Auditor
#   Cross-Platform Startup Script (Linux & macOS)
# =====================================================

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "====================================================="
echo "  Starting Domain Intelligence Agent & Screenshot Service"
echo "====================================================="
echo ""

# 1. Check if Node.js screenshot service is present
if [ -d "$SCRIPT_DIR/screenshot-service" ]; then
    echo "[1/2] Starting Node.js Puppeteer Screenshot Service on port 3000..."
    (cd "$SCRIPT_DIR/screenshot-service" && npm start) &
    NODE_PID=$!
    echo "Puppeteer service started (PID: $NODE_PID)"
    sleep 2
else
    echo "[1/2] Screenshot service directory not found. Skipping local Node.js service."
fi

# 2. Launch Streamlit Application
echo "[2/2] Starting Streamlit App..."
echo ""

cleanup() {
    echo ""
    echo "Stopping services..."
    if [ -n "$NODE_PID" ]; then
        kill "$NODE_PID" 2>/dev/null || true
    fi
    exit 0
}

trap cleanup INT TERM EXIT

cd "$SCRIPT_DIR/agent"
python3 -m streamlit run app.py
