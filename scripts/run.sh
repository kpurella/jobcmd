#!/bin/bash
echo "🚀 Starting JobCMD..."

# Start backend in background
cd backend
python main.py &
BACKEND_PID=$!
cd ..

sleep 2
echo "✅ Backend running at http://localhost:8000"
echo "📖 API docs: http://localhost:8000/docs"

# Open frontend
if command -v open &>/dev/null; then
  open frontend/index.html
elif command -v xdg-open &>/dev/null; then
  xdg-open frontend/index.html
else
  echo "🌐 Open frontend/index.html in your browser"
fi

echo ""
echo "Press Ctrl+C to stop."
trap "kill $BACKEND_PID 2>/dev/null" EXIT
wait $BACKEND_PID
