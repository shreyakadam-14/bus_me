# database_manager.py (complete version)
import sqlite3
import os
import datetime
from contextlib import contextmanager

class DatabaseConnection:
    """Simple database connection for basic operations"""
    
    def __init__(self):
        self.db_path = os.path.join('data', 'bus_management.db')
        os.makedirs('data', exist_ok=True)
        print("✓ DatabaseConnection initialized")
    
    @contextmanager
    def get_connection(self):
        """Get database connection"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def fetch_all(self, query, params=()):
        """Fetch all results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query, params=()):
        """Fetch one result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def execute_query(self, query, params=()):
        """Execute a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor


class DatabaseManager:
    """Main database manager with full functionality"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.db_path = os.path.join('data', 'bus_management.db')
        self.ensure_data_directory()
        self.init_database()
        print("✓ DatabaseManager initialized")
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Get database connection"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Initialize database and create tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    role TEXT NOT NULL,
                    status TEXT DEFAULT 'Active',
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Buses table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS buses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE NOT NULL,
                    bus_number TEXT UNIQUE NOT NULL,
                    model TEXT,
                    capacity INTEGER,
                    year INTEGER,
                    color TEXT,
                    status TEXT DEFAULT 'Active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Drivers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    license_number TEXT UNIQUE NOT NULL,
                    license_expiry DATE,
                    license_type TEXT,
                    status TEXT DEFAULT 'Active',
                    experience_years INTEGER DEFAULT 0,
                    joining_date DATE,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Schools table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    school_code TEXT UNIQUE NOT NULL,
                    type TEXT,
                    address TEXT,
                    city TEXT,
                    phone TEXT,
                    email TEXT,
                    contact_person TEXT,
                    contact_phone TEXT,
                    student_count INTEGER DEFAULT 0,
                    contract_status TEXT DEFAULT 'Active',
                    monthly_fee REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insurance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insurance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_id INTEGER,
                    policy_number TEXT UNIQUE,
                    provider TEXT,
                    coverage_amount REAL,
                    premium_amount REAL,
                    start_date DATE,
                    expiry_date DATE,
                    status TEXT DEFAULT 'Active',
                    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE
                )
            ''')
            
            # Bus assignments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bus_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_id INTEGER,
                    school_id INTEGER,
                    driver_id INTEGER,
                    pickup_time TIME,
                    drop_time TIME,
                    assigned_date DATE,
                    status TEXT DEFAULT 'Active',
                    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE,
                    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL
                )
            ''')
            
            # Activity logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    action TEXT,
                    module TEXT,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # System settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE,
                    setting_value TEXT,
                    setting_type TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Saved reports table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_name TEXT,
                    report_type TEXT,
                    report_data TEXT,
                    format TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
            # Insert default users if none exist
            self.insert_default_users()
            self.insert_default_settings()
    
    def insert_default_users(self):
        """Insert default users if table is empty"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                default_users = [
                    ('admin', 'admin123', 'System Administrator', 'admin@busmgmt.com', 'Super Admin'),
                    ('manager', 'manager123', 'Operations Manager', 'manager@busmgmt.com', 'Manager'),
                    ('viewer', 'viewer123', 'Report Viewer', 'viewer@busmgmt.com', 'Viewer')
                ]
                
                for username, password, full_name, email, role in default_users:
                    cursor.execute('''
                        INSERT INTO users (username, password, full_name, email, role)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (username, password, full_name, email, role))
                
                conn.commit()
                print("✓ Default users created")
    
    def insert_default_settings(self):
        """Insert default system settings"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM system_settings")
            if cursor.fetchone()[0] == 0:
                default_settings = [
                    ('company_name', 'Bus Management System Inc.', 'string', 'Company name'),
                    ('company_email', 'info@busmgmt.com', 'string', 'Company email'),
                    ('company_phone', '+1-555-123-4567', 'string', 'Company phone'),
                    ('session_timeout', '30', 'integer', 'Session timeout in minutes'),
                    ('date_format', 'YYYY-MM-DD', 'string', 'Date format'),
                    ('currency', 'USD ($)', 'string', 'Default currency')
                ]
                
                for key, value, type_, desc in default_settings:
                    cursor.execute('''
                        INSERT INTO system_settings (setting_key, setting_value, setting_type, description)
                        VALUES (?, ?, ?, ?)
                    ''', (key, value, type_, desc))
                
                conn.commit()
                print("✓ Default settings created")
    
    def execute_query(self, query, params=()):
        """Execute a query and return cursor"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def fetch_all(self, query, params=()):
        """Fetch all results"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query, params=()):
        """Fetch one result"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def insert(self, table, data):
        """Insert data"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def update(self, table, data, where_clause, where_params):
        """Update data"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            params = list(data.values()) + where_params
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def delete(self, table, where_clause, where_params):
        """Delete data"""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, where_params)
            conn.commit()
            return cursor.rowcount
    
    def table_exists(self, table_name):
        """Check if table exists"""
        result = self.fetch_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,)
        )
        return result is not None
    
    def get_table_names(self):
        """Get all table names"""
        tables = self.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        return [t['name'] for t in tables]
    
    def get_database_size(self):
        """Get database file size"""
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path)
        return 0