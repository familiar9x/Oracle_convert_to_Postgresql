#!/bin/bash

# Script để cấu hình database credentials

echo "=========================================="
echo "Database Configuration"
echo "=========================================="
echo ""
echo "Vui lòng nhập thông tin kết nối database:"
echo ""

# PostgreSQL
echo "--- PostgreSQL Configuration ---"
read -p "PostgreSQL Database Name [postgres]: " PG_DATABASE
PG_DATABASE=${PG_DATABASE:-postgres}

read -p "PostgreSQL Username [postgres]: " PG_USER
PG_USER=${PG_USER:-postgres}

read -sp "PostgreSQL Password: " PG_PASSWORD
echo ""

# Oracle
echo ""
echo "--- Oracle Configuration ---"
read -p "Oracle Service Name [ORCL]: " ORACLE_SERVICE
ORACLE_SERVICE=${ORACLE_SERVICE:-ORCL}

read -p "Oracle Username [system]: " ORACLE_USER
ORACLE_USER=${ORACLE_USER:-system}

read -sp "Oracle Password: " ORACLE_PASSWORD
echo ""

# Create .env file
echo ""
echo "Creating .env file..."

cat > .env << EOF
# PostgreSQL Configuration
PG_HOST=10.50.122.55
PG_PORT=5432
PG_DATABASE=$PG_DATABASE
PG_USER=$PG_USER
PG_PASSWORD=$PG_PASSWORD

# Oracle Configuration
ORACLE_HOST=10.50.122.51
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=$ORACLE_SERVICE
ORACLE_USER=$ORACLE_USER
ORACLE_PASSWORD=$ORACLE_PASSWORD
EOF

echo "✓ Configuration saved to .env"
echo ""
echo "Testing connections..."
echo ""

# Test connections
source venv/bin/activate
cd src
python db_connector.py

echo ""
echo "Configuration complete!"
