# database.py
import sqlite3
import os
import datetime
from contextlib import contextmanager

class Database:
    """Database manager for Bus Management System"""
    
    def __init__(self, db_path="bus_management.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create all tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ==================== USERS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    role TEXT NOT NULL CHECK(role IN ('Super Admin', 'Admin', 'Manager', 'Accountant', 'Driver', 'Viewer')),
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'Locked')),
                    last_login TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ==================== BUSES TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS buses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    registration_number TEXT UNIQUE NOT NULL,
                    bus_number TEXT UNIQUE NOT NULL,
                    model TEXT,
                    capacity INTEGER CHECK(capacity > 0),
                    year INTEGER,
                    color TEXT,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'Maintenance', 'Repair')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ==================== INSURANCE TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS insurance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_id INTEGER NOT NULL,
                    policy_number TEXT UNIQUE NOT NULL,
                    provider TEXT NOT NULL,
                    coverage_amount REAL CHECK(coverage_amount >= 0),
                    premium_amount REAL CHECK(premium_amount >= 0),
                    start_date DATE NOT NULL,
                    expiry_date DATE NOT NULL,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Expired', 'Cancelled')),
                    document_path TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
                    CHECK(start_date <= expiry_date)
                )
            ''')
            
            # ==================== DRIVERS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS drivers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    license_number TEXT UNIQUE NOT NULL,
                    license_expiry DATE NOT NULL,
                    license_type TEXT,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave', 'Suspended')),
                    experience_years INTEGER DEFAULT 0,
                    joining_date DATE NOT NULL,
                    bank_account TEXT,
                    ifsc_code TEXT,
                    address TEXT,
                    emergency_contact_name TEXT,
                    emergency_contact_phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # ==================== SCHOOLS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    school_code TEXT UNIQUE NOT NULL,
                    type TEXT CHECK(type IN ('Private', 'Government', 'International', 'CBSE', 'ICSE', 'State Board')),
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    principal_name TEXT,
                    contact_person TEXT,
                    contact_person_phone TEXT,
                    student_count INTEGER DEFAULT 0,
                    contract_status TEXT DEFAULT 'Active' CHECK(contract_status IN ('Active', 'Inactive', 'Expiring Soon', 'Negotiation', 'Terminated')),
                    contract_start DATE,
                    contract_end DATE,
                    monthly_fee REAL DEFAULT 0,
                    payment_status TEXT DEFAULT 'Paid' CHECK(payment_status IN ('Paid', 'Pending', 'Overdue', 'Partially Paid')),
                    billing_address TEXT,
                    gst_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CHECK(contract_start <= contract_end)
                )
            ''')
            
            # ==================== BUS ASSIGNMENTS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bus_assignments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_id INTEGER NOT NULL,
                    driver_id INTEGER,
                    school_id INTEGER NOT NULL,
                    assignment_type TEXT CHECK(assignment_type IN ('Permanent', 'Temporary', 'Backup')),
                    pickup_time TIME,
                    drop_time TIME,
                    route_description TEXT,
                    assigned_date DATE NOT NULL,
                    end_date DATE,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Completed', 'Cancelled')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
                    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE CASCADE
                )
            ''')
            
            # ==================== FINANCIAL TRANSACTIONS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_number TEXT UNIQUE NOT NULL,
                    transaction_type TEXT CHECK(transaction_type IN ('Income', 'Expense', 'Investment', 'Loan')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    description TEXT,
                    payment_method TEXT CHECK(payment_method IN ('Cash', 'Bank Transfer', 'Cheque', 'Credit Card', 'Online')),
                    reference_number TEXT,
                    transaction_date DATE NOT NULL,
                    school_id INTEGER,
                    bus_id INTEGER,
                    driver_id INTEGER,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (school_id) REFERENCES schools(id) ON DELETE SET NULL,
                    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE SET NULL,
                    FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE SET NULL,
                    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # ==================== ACTIVITY LOGS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    ip_address TEXT,
                    action TEXT NOT NULL,
                    module TEXT NOT NULL,
                    details TEXT,
                    status TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # ==================== SYSTEM SETTINGS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key TEXT UNIQUE NOT NULL,
                    setting_value TEXT,
                    setting_type TEXT,
                    description TEXT,
                    updated_by INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_buses_status ON buses(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_schools_city ON schools(city)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_insurance_expiry ON insurance(expiry_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_bus ON bus_assignments(bus_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_school ON bus_assignments(school_id)')
            
            conn.commit()
            
            # Insert default data if needed
            self.insert_default_data()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
        finally:
            conn.close()
    
    def insert_default_data(self):
        """Insert default data for initial setup"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if users table is empty
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Insert default admin user
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, email, role, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('admin', 'admin123', 'System Administrator', 'admin@busmgmt.com', 'Super Admin', 'Active'))
                
                # Insert default manager
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, email, role, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('manager', 'manager123', 'Operations Manager', 'manager@busmgmt.com', 'Manager', 'Active'))
                
                # Insert default viewer
                cursor.execute('''
                    INSERT INTO users (username, password, full_name, email, role, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', ('viewer', 'viewer123', 'Report Viewer', 'viewer@busmgmt.com', 'Viewer', 'Active'))
            
            # Insert default system settings
            default_settings = [
                ('company_name', 'Bus Management System Inc.', 'string', 'Company name for invoices'),
                ('company_address', '123 Business Street, City, State 12345', 'text', 'Company address'),
                ('company_phone', '+1-555-123-4567', 'string', 'Company phone number'),
                ('company_email', 'info@busmgmt.com', 'string', 'Company email'),
                ('tax_rate', '18.0', 'float', 'Default tax rate percentage'),
                ('currency', 'USD ($)', 'string', 'Default currency'),
                ('date_format', 'YYYY-MM-DD', 'string', 'Date display format'),
                ('session_timeout', '30', 'integer', 'Session timeout in minutes'),
                ('auto_backup', 'true', 'boolean', 'Enable automatic backups'),
                ('backup_path', './backups/', 'string', 'Backup directory path')
            ]
            
            for key, value, type_, desc in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO system_settings (setting_key, setting_value, setting_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (key, value, type_, desc))
            
            conn.commit()
    
    def execute_query(self, query, params=()):
        """Execute a query and return cursor"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor
    
    def fetch_all(self, query, params=()):
        """Fetch all results from a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def fetch_one(self, query, params=()):
        """Fetch one result from a query"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def insert(self, table, data):
        """Insert data into table"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, list(data.values()))
            conn.commit()
            return cursor.lastrowid
    
    def update(self, table, data, where_clause, where_params):
        """Update data in table"""
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            params = list(data.values()) + where_params
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def delete(self, table, where_clause, where_params):
        """Delete data from table"""
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, where_params)
            conn.commit()
            return cursor.rowcount