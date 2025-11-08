#!/bin/bash

# Script hướng dẫn cài đặt và setup project

echo "=========================================="
echo "Oracle to PostgreSQL Converter - Setup"
echo "=========================================="
echo ""

# Kiểm tra Python
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found: $PYTHON_VERSION"
else
    echo "✗ Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Tạo virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Create .env file if not exists
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your database credentials:"
    echo "   nano .env"
else
    echo "✓ .env file already exists"
fi

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p output
echo "✓ Output directory ready"

# Test import
echo ""
echo "Testing Python imports..."
python3 -c "import psycopg2; import cx_Oracle; import sqlparse" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ All Python packages imported successfully"
else
    echo "⚠️  Some packages may need additional setup"
    echo ""
    echo "For Oracle (cx_Oracle), you may need to install Oracle Instant Client:"
    echo "  - Download from: https://www.oracle.com/database/technologies/instant-client/downloads.html"
    echo "  - Follow installation instructions for your OS"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials:"
echo "   nano .env"
echo ""
echo "2. Activate virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "3. Test database connections:"
echo "   cd src && python db_connector.py"
echo ""
echo "4. Run the main program:"
echo "   cd src && python main.py"
echo ""
echo "5. Run tests:"
echo "   pytest tests/test_converter.py -v"
echo ""
