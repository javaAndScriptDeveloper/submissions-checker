#!/bin/bash
# Development environment setup script

set -e  # Exit on error

echo "🚀 Setting up Submissions Checker development environment..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install uv first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
    echo "🔧 Creating virtual environment..."
    uv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Install dependencies
echo "📦 Installing dependencies with uv..."
uv pip install -e ".[dev]"
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please update .env with your configuration (API keys, secrets, etc.)"
    echo ""
else
    echo "✅ .env file already exists"
    echo ""
fi

# Start Docker Compose services
echo "🐳 Starting Docker Compose services..."
docker compose up -d postgres
echo "✅ Docker services started"
echo ""

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5
echo "✅ PostgreSQL ready"
echo ""

echo "ℹ️  Note: Database migrations will run automatically when the app starts"
echo ""

# Display next steps
echo "✅ Development environment setup complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "  1. Update .env file with your configuration:"
echo "     - Set GITHUB_WEBHOOK_SECRET"
echo "     - Set OPENAI_API_KEY (if using AI features)"
echo "     - Update other settings as needed"
echo ""
echo "  2. Start development server (migrations run automatically on startup):"
echo "     make dev"
echo ""
echo "  3. View API documentation:"
echo "     http://localhost:8000/docs"
echo ""
echo "  4. Run tests:"
echo "     make test"
echo ""
echo "Available make commands:"
echo "  make install        - Install dependencies"
echo "  make dev           - Start development server"
echo "  make up            - Start all Docker services"
echo "  make down          - Stop all Docker services"
echo "  make test          - Run tests"
echo "  make migrate       - Run migrations"
echo "  make lint          - Run linting"
echo "  make format        - Format code"
echo ""
