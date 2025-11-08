"""
Oracle to PostgreSQL converter
Converts Oracle functions and procedures to PostgreSQL compatible syntax
"""
import re
import sqlparse
from typing import Dict, List


class OracleToPostgreSQLConverter:
    """Convert Oracle PL/SQL to PostgreSQL PL/pgSQL"""
    
    def __init__(self):
        self.conversion_log = []
    
    def convert_procedure(self, oracle_code: str) -> str:
        """
        Convert Oracle procedure/function to PostgreSQL
        
        Args:
            oracle_code: Oracle PL/SQL code
            
        Returns:
            PostgreSQL PL/pgSQL code
        """
        converted = oracle_code
        
        # Log original
        self.conversion_log.append("=== Original Oracle Code ===")
        self.conversion_log.append(oracle_code)
        
        # Apply conversions
        converted = self._convert_create_statement(converted)
        converted = self._convert_data_types(converted)
        converted = self._convert_variable_declarations(converted)
        converted = self._convert_cursor_syntax(converted)
        converted = self._convert_exception_handling(converted)
        converted = self._convert_string_functions(converted)
        converted = self._convert_date_functions(converted)
        converted = self._convert_null_functions(converted)
        converted = self._convert_sequences(converted)
        converted = self._convert_dual_table(converted)
        converted = self._convert_rownum(converted)
        converted = self._format_code(converted)
        
        # Log converted
        self.conversion_log.append("\n=== Converted PostgreSQL Code ===")
        self.conversion_log.append(converted)
        
        return converted
    
    def _convert_create_statement(self, code: str) -> str:
        """Convert CREATE PROCEDURE/FUNCTION syntax"""
        # Oracle: CREATE OR REPLACE PROCEDURE proc_name
        # PostgreSQL: CREATE OR REPLACE FUNCTION proc_name
        
        # Convert PROCEDURE to FUNCTION
        code = re.sub(
            r'CREATE(\s+OR\s+REPLACE)?\s+PROCEDURE\s+',
            r'CREATE\1 FUNCTION ',
            code,
            flags=re.IGNORECASE
        )
        
        # Add RETURNS clause if missing (for procedures converted to functions)
        if re.search(r'CREATE.*FUNCTION', code, re.IGNORECASE) and \
           not re.search(r'RETURNS', code, re.IGNORECASE):
            # Find the AS/IS keyword and add RETURNS VOID before it
            code = re.sub(
                r'(\))\s*(AS|IS)',
                r'\1 RETURNS VOID AS',
                code,
                flags=re.IGNORECASE
            )
        
        # Change AS/IS to $$
        code = re.sub(
            r'\s+(AS|IS)\s+',
            r' AS $$\n',
            code,
            flags=re.IGNORECASE
        )
        
        # Add language clause at the end
        if not re.search(r'LANGUAGE\s+plpgsql', code, re.IGNORECASE):
            code = code.rstrip()
            if not code.endswith('$$'):
                code += '\n$$'
            code += ' LANGUAGE plpgsql;'
        
        return code
    
    def _convert_data_types(self, code: str) -> str:
        """Convert Oracle data types to PostgreSQL equivalents"""
        conversions = {
            r'\bNUMBER\b': 'NUMERIC',
            r'\bVARCHAR2\b': 'VARCHAR',
            r'\bCLOB\b': 'TEXT',
            r'\bBLOB\b': 'BYTEA',
            r'\bDATE\b': 'TIMESTAMP',
            r'\bRAW\b': 'BYTEA',
            r'\bLONG\b': 'TEXT',
            r'\bINTEGER\b': 'INTEGER',
            r'\bBINARY_INTEGER\b': 'INTEGER',
            r'\bPLS_INTEGER\b': 'INTEGER',
        }
        
        for oracle_type, pg_type in conversions.items():
            code = re.sub(oracle_type, pg_type, code, flags=re.IGNORECASE)
        
        return code
    
    def _convert_variable_declarations(self, code: str) -> str:
        """Convert variable declaration syntax"""
        # Oracle: var_name TYPE := value;
        # PostgreSQL: var_name TYPE := value; (mostly same, but some adjustments)
        
        # Add DECLARE section if variables are declared
        if re.search(r'^\s*\w+\s+\w+.*;', code, re.MULTILINE):
            if not re.search(r'DECLARE', code, re.IGNORECASE):
                code = re.sub(
                    r'(\$\$\s*\n)',
                    r'\1DECLARE\n',
                    code
                )
        
        return code
    
    def _convert_cursor_syntax(self, code: str) -> str:
        """Convert cursor syntax"""
        # Oracle: CURSOR cur_name IS SELECT...
        # PostgreSQL: cur_name CURSOR FOR SELECT...
        
        code = re.sub(
            r'CURSOR\s+(\w+)\s+IS\s+',
            r'\1 CURSOR FOR ',
            code,
            flags=re.IGNORECASE
        )
        
        return code
    
    def _convert_exception_handling(self, code: str) -> str:
        """Convert exception handling"""
        # Oracle: WHEN OTHERS THEN
        # PostgreSQL: Similar, but different exception names
        
        conversions = {
            r'NO_DATA_FOUND': 'NO_DATA_FOUND',
            r'TOO_MANY_ROWS': 'TOO_MANY_ROWS',
            r'DUP_VAL_ON_INDEX': 'UNIQUE_VIOLATION',
            r'WHEN\s+OTHERS': 'WHEN OTHERS',
        }
        
        for oracle_ex, pg_ex in conversions.items():
            code = re.sub(oracle_ex, pg_ex, code, flags=re.IGNORECASE)
        
        return code
    
    def _convert_string_functions(self, code: str) -> str:
        """Convert Oracle string functions to PostgreSQL"""
        conversions = {
            r'\|\|': '||',  # Concatenation (same)
            r'SUBSTR\s*\(': 'SUBSTRING(',
            r'LENGTH\s*\(': 'LENGTH(',  # Same
            r'INSTR\s*\(': 'POSITION(',
            r'LTRIM\s*\(': 'LTRIM(',  # Same
            r'RTRIM\s*\(': 'RTRIM(',  # Same
            r'UPPER\s*\(': 'UPPER(',  # Same
            r'LOWER\s*\(': 'LOWER(',  # Same
        }
        
        for oracle_func, pg_func in conversions.items():
            code = re.sub(oracle_func, pg_func, code, flags=re.IGNORECASE)
        
        return code
    
    def _convert_date_functions(self, code: str) -> str:
        """Convert Oracle date functions to PostgreSQL"""
        # SYSDATE -> CURRENT_TIMESTAMP or NOW()
        code = re.sub(r'\bSYSDATE\b', 'CURRENT_TIMESTAMP', code, flags=re.IGNORECASE)
        
        # TO_DATE -> TO_TIMESTAMP or TO_DATE (PostgreSQL has both)
        # Keep as is, but note: formats might need adjustment
        
        # TO_CHAR for dates
        # Keep as is, but formats might differ
        
        # ADD_MONTHS -> + INTERVAL
        # This requires more complex parsing
        
        return code
    
    def _convert_null_functions(self, code: str) -> str:
        """Convert NULL handling functions"""
        # NVL(expr1, expr2) -> COALESCE(expr1, expr2)
        code = re.sub(r'\bNVL\s*\(', 'COALESCE(', code, flags=re.IGNORECASE)
        
        # NVL2(expr1, expr2, expr3) -> CASE WHEN expr1 IS NOT NULL THEN expr2 ELSE expr3 END
        # This is complex, keeping NVL2 for manual review
        
        return code
    
    def _convert_sequences(self, code: str) -> str:
        """Convert sequence syntax"""
        # Oracle: seq_name.NEXTVAL
        # PostgreSQL: NEXTVAL('seq_name')
        
        code = re.sub(
            r'(\w+)\.NEXTVAL',
            r"NEXTVAL('\1')",
            code,
            flags=re.IGNORECASE
        )
        
        code = re.sub(
            r'(\w+)\.CURRVAL',
            r"CURRVAL('\1')",
            code,
            flags=re.IGNORECASE
        )
        
        return code
    
    def _convert_dual_table(self, code: str) -> str:
        """Convert DUAL table references"""
        # Oracle: SELECT ... FROM DUAL
        # PostgreSQL: SELECT ... (no FROM needed for expressions)
        
        code = re.sub(
            r'\s+FROM\s+DUAL\b',
            '',
            code,
            flags=re.IGNORECASE
        )
        
        return code
    
    def _convert_rownum(self, code: str) -> str:
        """Convert ROWNUM to PostgreSQL equivalent"""
        # Oracle: WHERE ROWNUM <= n
        # PostgreSQL: LIMIT n
        
        # Simple case: WHERE ROWNUM <= number
        code = re.sub(
            r'WHERE\s+ROWNUM\s*<=\s*(\d+)',
            r'LIMIT \1',
            code,
            flags=re.IGNORECASE
        )
        
        return code
    
    def _format_code(self, code: str) -> str:
        """Format the SQL code"""
        try:
            formatted = sqlparse.format(
                code,
                reindent=True,
                keyword_case='upper'
            )
            return formatted
        except:
            return code
    
    def get_conversion_log(self) -> List[str]:
        """Get the conversion log"""
        return self.conversion_log
    
    def clear_log(self):
        """Clear the conversion log"""
        self.conversion_log = []


def convert_file(input_file: str, output_file: str):
    """
    Convert an Oracle SQL file to PostgreSQL
    
    Args:
        input_file: Path to Oracle SQL file
        output_file: Path to output PostgreSQL SQL file
    """
    converter = OracleToPostgreSQLConverter()
    
    with open(input_file, 'r') as f:
        oracle_code = f.read()
    
    pg_code = converter.convert_procedure(oracle_code)
    
    with open(output_file, 'w') as f:
        f.write(pg_code)
    
    print(f"✓ Converted {input_file} -> {output_file}")
    print("\nConversion log:")
    for log in converter.get_conversion_log():
        print(log)


if __name__ == "__main__":
    # Example usage
    print("Oracle to PostgreSQL Converter")
    print("Usage: python converter.py <input_file> <output_file>")
