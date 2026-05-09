#!/bin/bash
set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   JobCMD — AI Job Search Command Center  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then echo "❌ Python 3 required"; exit 1; fi
echo "✅ Python: $(python3 --version)"

# Install backend
echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt -q
cd ..

# Setup data
mkdir -p data
cp data/sample/profile.json data/profile.json 2>/dev/null || true
echo "✅ Data directory initialized"

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo ""
  echo "⚠️  ANTHROPIC_API_KEY not set. AI features will use simulation mode."
  echo "   Set it with: export ANTHROPIC_API_KEY=sk-ant-..."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start:"
echo "  Backend:  cd backend && python main.py"
echo "  Frontend: open frontend/index.html in browser"
echo ""
echo "Or run both with: ./scripts/run.sh"
