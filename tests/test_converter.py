"""
Test suite for Oracle to PostgreSQL conversion
"""
import pytest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from converter import OracleToPostgreSQLConverter


class TestConverter:
    
    def setup_method(self):
        """Setup for each test"""
        self.converter = OracleToPostgreSQLConverter()
    
    def test_convert_procedure_to_function(self):
        """Test converting Oracle PROCEDURE to PostgreSQL FUNCTION"""
        oracle_code = """
        CREATE OR REPLACE PROCEDURE test_proc (p_id IN NUMBER)
        AS
        BEGIN
            NULL;
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'CREATE OR REPLACE FUNCTION' in result.upper()
        assert 'RETURNS VOID' in result.upper()
        assert 'LANGUAGE plpgsql' in result.lower()
    
    def test_convert_data_types(self):
        """Test data type conversions"""
        oracle_code = """
        CREATE OR REPLACE FUNCTION test_func (p_name IN VARCHAR2)
        RETURN NUMBER
        AS
            v_count NUMBER;
        BEGIN
            RETURN v_count;
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'VARCHAR2' not in result.upper()
        assert 'VARCHAR' in result.upper() or 'TEXT' in result.upper()
        assert 'NUMERIC' in result.upper()
    
    def test_convert_sysdate(self):
        """Test SYSDATE conversion"""
        oracle_code = """
        CREATE OR REPLACE FUNCTION get_current_date
        RETURN DATE
        AS
        BEGIN
            RETURN SYSDATE;
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'SYSDATE' not in result.upper()
        assert 'CURRENT_TIMESTAMP' in result.upper()
    
    def test_convert_nvl(self):
        """Test NVL to COALESCE conversion"""
        oracle_code = """
        CREATE OR REPLACE FUNCTION test_nvl (p_val IN NUMBER)
        RETURN NUMBER
        AS
        BEGIN
            RETURN NVL(p_val, 0);
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'NVL' not in result.upper()
        assert 'COALESCE' in result.upper()
    
    def test_convert_sequence(self):
        """Test sequence syntax conversion"""
        oracle_code = """
        CREATE OR REPLACE PROCEDURE insert_record
        AS
            v_id NUMBER;
        BEGIN
            v_id := seq_id.NEXTVAL;
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'seq_id.NEXTVAL' not in result
        assert "NEXTVAL('seq_id')" in result
    
    def test_convert_dual(self):
        """Test DUAL table removal"""
        oracle_code = """
        CREATE OR REPLACE FUNCTION test_dual
        RETURN NUMBER
        AS
            v_result NUMBER;
        BEGIN
            SELECT 1 INTO v_result FROM DUAL;
            RETURN v_result;
        END;
        """
        
        result = self.converter.convert_procedure(oracle_code)
        
        assert 'FROM DUAL' not in result.upper()


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
