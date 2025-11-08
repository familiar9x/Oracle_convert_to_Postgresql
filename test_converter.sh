#!/bin/bash

# Quick test script for the converter

echo "=========================================="
echo "Testing Oracle to PostgreSQL Converter"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Test converter with example files
echo "Testing converter with example Oracle files..."
echo ""

cd src

# Test function conversion
echo "1. Converting get_employee_fullname function..."
python3 << EOF
from converter import convert_file
import os

oracle_file = '../examples/oracle_function_examples.sql'
output_file = '../examples/converted_functions.sql'

if os.path.exists(oracle_file):
    try:
        convert_file(oracle_file, output_file)
        print("\n✓ Conversion successful!")
        print(f"Output: {output_file}")
    except Exception as e:
        print(f"\n✗ Conversion failed: {e}")
else:
    print(f"✗ File not found: {oracle_file}")
EOF

echo ""
echo "2. Converting calculate_salary_bonus procedure..."
python3 << EOF
from converter import convert_file
import os

oracle_file = '../examples/oracle_procedure_example.sql'
output_file = '../examples/converted_procedure.sql'

if os.path.exists(oracle_file):
    try:
        convert_file(oracle_file, output_file)
        print("\n✓ Conversion successful!")
        print(f"Output: {output_file}")
    except Exception as e:
        print(f"\n✗ Conversion failed: {e}")
else:
    print(f"✗ File not found: {oracle_file}")
EOF

echo ""
echo "=========================================="
echo "Running unit tests..."
echo "=========================================="
cd ..
pytest tests/test_converter.py -v

echo ""
echo "=========================================="
echo "Test complete!"
echo "=========================================="
echo ""
echo "Check the examples/ directory for converted files:"
echo "  - examples/converted_functions.sql"
echo "  - examples/converted_procedure.sql"
echo ""
