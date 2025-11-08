"""
Main script to extract Oracle procedures/functions and convert to PostgreSQL
"""
import os
import sys
from pathlib import Path
from db_connector import OracleConnector, PostgreSQLConnector
from converter import OracleToPostgreSQLConverter


def extract_and_convert(owner=None, output_dir='output'):
    """
    Extract procedures/functions from Oracle and convert to PostgreSQL
    
    Args:
        owner: Oracle schema owner (optional)
        output_dir: Directory to save converted files
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Connect to Oracle
    print("\n=== Connecting to Oracle ===")
    oracle = OracleConnector()
    if not oracle.connect():
        print("Failed to connect to Oracle. Exiting.")
        return
    
    try:
        # Get list of procedures/functions
        print(f"\n=== Fetching procedures/functions from Oracle ===")
        procedures = oracle.get_procedures(owner)
        
        if not procedures:
            print("No procedures/functions found.")
            return
        
        print(f"Found {len(procedures)} objects:")
        for proc in procedures:
            print(f"  - {proc['OBJECT_NAME']} ({proc['OBJECT_TYPE']}) - {proc['STATUS']}")
        
        # Convert each procedure
        converter = OracleToPostgreSQLConverter()
        
        print(f"\n=== Converting procedures ===")
        for proc in procedures:
            obj_name = proc['OBJECT_NAME']
            obj_type = proc['OBJECT_TYPE']
            
            print(f"\nProcessing {obj_name} ({obj_type})...")
            
            # Get source code
            source = oracle.get_procedure_source(obj_name, owner)
            
            if not source:
                print(f"  ✗ Could not retrieve source for {obj_name}")
                continue
            
            # Save original Oracle code
            oracle_file = os.path.join(output_dir, f"{obj_name}_oracle.sql")
            with open(oracle_file, 'w') as f:
                f.write(source)
            print(f"  ✓ Saved Oracle source: {oracle_file}")
            
            # Convert to PostgreSQL
            converter.clear_log()
            pg_code = converter.convert_procedure(source)
            
            # Save PostgreSQL code
            pg_file = os.path.join(output_dir, f"{obj_name}_postgresql.sql")
            with open(pg_file, 'w') as f:
                f.write(pg_code)
            print(f"  ✓ Saved PostgreSQL version: {pg_file}")
            
            # Save conversion log
            log_file = os.path.join(output_dir, f"{obj_name}_conversion.log")
            with open(log_file, 'w') as f:
                f.write('\n'.join(converter.get_conversion_log()))
            print(f"  ✓ Saved conversion log: {log_file}")
        
        print(f"\n=== Conversion Complete ===")
        print(f"Output directory: {output_dir}")
        
    finally:
        oracle.disconnect()


def test_converted_procedure(pg_file, test_data=None):
    """
    Test a converted procedure on PostgreSQL
    
    Args:
        pg_file: Path to PostgreSQL SQL file
        test_data: Optional test data parameters
    """
    print(f"\n=== Testing {pg_file} on PostgreSQL ===")
    
    # Connect to PostgreSQL
    pg = PostgreSQLConnector()
    if not pg.connect():
        print("Failed to connect to PostgreSQL. Exiting.")
        return
    
    try:
        # Read and execute the converted SQL
        with open(pg_file, 'r') as f:
            pg_code = f.read()
        
        print("\nCreating function in PostgreSQL...")
        if pg.execute_script(pg_code):
            print("✓ Function created successfully")
            
            # If test data provided, execute the function
            if test_data:
                print("\nExecuting function with test data...")
                # Extract function name
                import re
                match = re.search(r'FUNCTION\s+(\w+)', pg_code, re.IGNORECASE)
                if match:
                    func_name = match.group(1)
                    test_query = f"SELECT {func_name}({test_data})"
                    result = pg.execute_query(test_query)
                    print(f"Result: {result}")
        else:
            print("✗ Failed to create function")
            
    finally:
        pg.disconnect()


def interactive_menu():
    """Interactive menu for user"""
    while True:
        print("\n" + "="*50)
        print("Oracle to PostgreSQL Converter")
        print("="*50)
        print("1. Test database connections")
        print("2. Extract and convert all procedures/functions")
        print("3. Extract and convert by schema owner")
        print("4. Convert a single SQL file")
        print("5. Test converted procedure on PostgreSQL")
        print("0. Exit")
        print("="*50)
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            from db_connector import test_connections
            test_connections()
            
        elif choice == '2':
            output = input("Output directory (default: output): ").strip() or 'output'
            extract_and_convert(owner=None, output_dir=output)
            
        elif choice == '3':
            owner = input("Enter schema owner: ").strip()
            output = input("Output directory (default: output): ").strip() or 'output'
            extract_and_convert(owner=owner, output_dir=output)
            
        elif choice == '4':
            input_file = input("Enter Oracle SQL file path: ").strip()
            output_file = input("Enter output PostgreSQL file path: ").strip()
            
            if os.path.exists(input_file):
                from converter import convert_file
                convert_file(input_file, output_file)
            else:
                print(f"File not found: {input_file}")
                
        elif choice == '5':
            pg_file = input("Enter PostgreSQL SQL file path: ").strip()
            test_data = input("Enter test parameters (optional): ").strip() or None
            
            if os.path.exists(pg_file):
                test_converted_procedure(pg_file, test_data)
            else:
                print(f"File not found: {pg_file}")
                
        elif choice == '0':
            print("Goodbye!")
            break
            
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    interactive_menu()
