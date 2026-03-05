# database_manager.py
import sqlite3
import os
import datetime
from contextlib import contextmanager

class DatabaseManager:
    """Central database manager for the entire application"""
    
    _instance = None  # Singleton pattern
    
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
        
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs('data', exist_ok=True)
    
    def init_database(self):
        """Initialize database and create all tables if they don't exist"""
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
            
            # ==================== SAVED REPORTS TABLE ====================
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS saved_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_name TEXT NOT NULL,
                    report_type TEXT NOT NULL,
                    generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    report_data TEXT,
                    format TEXT,
                    created_by TEXT
                )
            ''')
            
            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_buses_status ON buses(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_buses_number ON buses(bus_number)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_status ON drivers(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_drivers_license ON drivers(license_number)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_schools_city ON schools(city)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_schools_status ON schools(contract_status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_insurance_expiry ON insurance(expiry_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_insurance_bus ON insurance(bus_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_bus ON bus_assignments(bus_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_school ON bus_assignments(school_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_assignments_status ON bus_assignments(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_activity_logs_timestamp ON activity_logs(timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_activity_logs_user ON activity_logs(username)')
            
            conn.commit()
            
            # Insert default data if needed
            self.insert_default_data()
    
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
                
                print("✓ Default users created")
            
            # Insert default system settings
            default_settings = [
                ('company_name', 'Bus Management System Inc.', 'string', 'Company name for invoices'),
                ('company_address', '123 Business Street, City, State 12345', 'text', 'Company address'),
                ('company_phone', '+1-555-123-4567', 'string', 'Company phone number'),
                ('company_email', 'info@busmgmt.com', 'string', 'Company email'),
                ('company_website', 'www.busmgmt.com', 'string', 'Company website'),
                ('tax_id', 'TAX-123456789', 'string', 'Tax ID / VAT number'),
                ('tax_rate', '18.0', 'float', 'Default tax rate percentage'),
                ('currency', 'USD ($)', 'string', 'Default currency'),
                ('decimal_places', '2', 'integer', 'Number of decimal places'),
                ('date_format', 'YYYY-MM-DD', 'string', 'Date display format'),
                ('inv_prefix', 'INV', 'string', 'Invoice number prefix'),
                ('inv_start', '1001', 'integer', 'Starting invoice number'),
                ('payment_terms', 'Net 30', 'string', 'Default payment terms'),
                ('session_timeout', '30', 'integer', 'Session timeout in minutes'),
                ('auto_backup', 'true', 'boolean', 'Enable automatic backups'),
                ('backup_freq', 'Daily', 'string', 'Backup frequency'),
                ('backup_time', '02:00', 'string', 'Backup time'),
                ('retention', '30', 'integer', 'Backup retention days'),
                ('backup_path', './backups/', 'string', 'Backup directory path'),
                ('min_password', '8', 'integer', 'Minimum password length'),
                ('complex_password', 'false', 'boolean', 'Require complex passwords'),
                ('max_attempts', '3', 'integer', 'Maximum login attempts'),
                ('theme', 'Light', 'string', 'UI theme'),
                ('language', 'English', 'string', 'Default language')
            ]
            
            for key, value, type_, desc in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO system_settings (setting_key, setting_value, setting_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (key, value, type_, desc))
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            yield conn
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
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
    
    def insert_many(self, table, data_list):
        """Insert multiple rows into table"""
        if not data_list:
            return 0
        
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in data_list[0]])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        values_list = [list(data.values()) for data in data_list]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, values_list)
            conn.commit()
            return cursor.rowcount
    
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
    
    def table_exists(self, table_name):
        """Check if a table exists"""
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
    
    def get_table_info(self, table_name):
        """Get column information for a table"""
        return self.fetch_all(f"PRAGMA table_info({table_name})")
    
    def backup_database(self, backup_path=None):
        """Create a backup of the database"""
        if backup_path is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join('data', 'backups', f'backup_{timestamp}.db')
        
        # Create backup directory if needed
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Connect to source and destination
        source = sqlite3.connect(self.db_path)
        dest = sqlite3.connect(backup_path)
        
        # Perform backup
        source.backup(dest)
        
        source.close()
        dest.close()
        
        print(f"✓ Database backed up to: {backup_path}")
        return backup_path
    
    def restore_database(self, backup_path):
        """Restore database from backup"""
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file not found: {backup_path}")
        
        # Close any existing connections
        source = sqlite3.connect(backup_path)
        dest = sqlite3.connect(self.db_path)
        
        # Perform restore
        source.backup(dest)
        
        source.close()
        dest.close()
        
        print(f"✓ Database restored from: {backup_path}")
        return True
    
    def get_database_size(self):
        """Get database file size in bytes"""
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path)
        return 0
    
    def vacuum(self):
        """Vacuum the database to reclaim space"""
        with self.get_connection() as conn:
            conn.execute("VACUUM")
        print("✓ Database vacuumed")
    
    def begin_transaction(self):
        """Begin a transaction"""
        self._transaction_conn = sqlite3.connect(self.db_path)
        self._transaction_conn.row_factory = sqlite3.Row
        self._transaction_conn.execute("BEGIN TRANSACTION")
    
    def commit_transaction(self):
        """Commit the current transaction"""
        if hasattr(self, '_transaction_conn'):
            self._transaction_conn.commit()
            self._transaction_conn.close()
            delattr(self, '_transaction_conn')
    
    def rollback_transaction(self):
        """Rollback the current transaction"""
        if hasattr(self, '_transaction_conn'):
            self._transaction_conn.rollback()
            self._transaction_conn.close()
            delattr(self, '_transaction_conn')


# Example usage and testing
if __name__ == "__main__":
    print("Testing DatabaseManager...")
    
    # Create instance
    db = DatabaseManager()
    
    # Test connection
    print(f"Database path: {db.db_path}")
    print(f"Database size: {db.get_database_size()} bytes")
    
    # List tables
    tables = db.get_table_names()
    print(f"\nTables in database ({len(tables)}):")
    for table in tables:
        count = db.fetch_one(f"SELECT COUNT(*) as count FROM {table}")['count']
        print(f"  • {table}: {count} records")
    
    # Test users
    users = db.fetch_all("SELECT username, role, status FROM users")
    print(f"\nUsers ({len(users)}):")
    for user in users:
        print(f"  • {user['username']} - {user['role']} ({user['status']})")
    
    print("\n✓ DatabaseManager test complete")