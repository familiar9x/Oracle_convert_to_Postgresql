"""
Database connection utilities for PostgreSQL and Oracle
"""
import os
import cx_Oracle
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PostgreSQLConnector:
    """PostgreSQL database connector"""
    
    def __init__(self):
        self.host = os.getenv('PG_HOST', '10.50.122.55')
        self.port = os.getenv('PG_PORT', '5432')
        self.database = os.getenv('PG_DATABASE')
        self.user = os.getenv('PG_USER')
        self.password = os.getenv('PG_PASSWORD')
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print(f"✓ Connected to PostgreSQL at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ PostgreSQL connection error: {e}")
            return False
    
    def disconnect(self):
        """Close PostgreSQL connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ PostgreSQL connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"✗ Query execution error: {e}")
            return None
    
    def execute_command(self, command, params=None):
        """Execute INSERT/UPDATE/DELETE command"""
        try:
            self.cursor.execute(command, params)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"✗ Command execution error: {e}")
            return False
    
    def execute_script(self, script):
        """Execute SQL script"""
        try:
            self.cursor.execute(script)
            self.connection.commit()
            print("✓ Script executed successfully")
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"✗ Script execution error: {e}")
            return False


class OracleConnector:
    """Oracle database connector"""
    
    def __init__(self):
        self.host = os.getenv('ORACLE_HOST', '10.50.122.51')
        self.port = os.getenv('ORACLE_PORT', '1521')
        self.service_name = os.getenv('ORACLE_SERVICE_NAME')
        self.user = os.getenv('ORACLE_USER')
        self.password = os.getenv('ORACLE_PASSWORD')
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Oracle"""
        try:
            dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.service_name)
            self.connection = cx_Oracle.connect(
                user=self.user,
                password=self.password,
                dsn=dsn
            )
            self.cursor = self.connection.cursor()
            print(f"✓ Connected to Oracle at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"✗ Oracle connection error: {e}")
            return False
    
    def disconnect(self):
        """Close Oracle connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✓ Oracle connection closed")
    
    def execute_query(self, query, params=None):
        """Execute a SELECT query"""
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            columns = [col[0] for col in self.cursor.description]
            rows = self.cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"✗ Query execution error: {e}")
            return None
    
    def execute_command(self, command, params=None):
        """Execute INSERT/UPDATE/DELETE command"""
        try:
            if params:
                self.cursor.execute(command, params)
            else:
                self.cursor.execute(command)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"✗ Command execution error: {e}")
            return False
    
    def get_procedures(self, owner=None):
        """Get list of procedures from Oracle"""
        query = """
            SELECT object_name, object_type, status
            FROM all_objects
            WHERE object_type IN ('PROCEDURE', 'FUNCTION', 'PACKAGE')
        """
        if owner:
            query += f" AND owner = '{owner}'"
        query += " ORDER BY object_name"
        return self.execute_query(query)
    
    def get_procedure_source(self, name, owner=None):
        """Get source code of a procedure/function"""
        query = """
            SELECT text
            FROM all_source
            WHERE name = :name
        """
        if owner:
            query += " AND owner = :owner"
            params = {'name': name, 'owner': owner}
        else:
            params = {'name': name}
        query += " ORDER BY line"
        
        results = self.execute_query(query, params)
        if results:
            return ''.join([row['TEXT'] for row in results])
        return None


def test_connections():
    """Test both database connections"""
    print("\n=== Testing Database Connections ===\n")
    
    # Test PostgreSQL
    print("1. Testing PostgreSQL connection...")
    pg = PostgreSQLConnector()
    pg_status = pg.connect()
    if pg_status:
        pg.disconnect()
    
    print()
    
    # Test Oracle
    print("2. Testing Oracle connection...")
    oracle = OracleConnector()
    oracle_status = oracle.connect()
    if oracle_status:
        oracle.disconnect()
    
    print("\n=== Connection Test Complete ===\n")
    return pg_status and oracle_status


if __name__ == "__main__":
    test_connections()
