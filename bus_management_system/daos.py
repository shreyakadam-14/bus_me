# daos.py
import datetime
from database_manager import DatabaseManager

class BaseDAO:
    """Base class for all DAOs"""
    
    def __init__(self):
        self.db = DatabaseManager()
        
    def log_activity(self, action, module, details, username="system"):
        """Log user activity"""
        try:
            log_data = {
                'username': username,
                'action': action,
                'module': module,
                'details': details,
                'timestamp': datetime.datetime.now().isoformat()
            }
            # Check if activity_logs table exists
            tables = self.db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_logs'")
            if tables:
                self.db.insert('activity_logs', log_data)
        except Exception as e:
            print(f"Logging error (non-critical): {e}")


class UserDAO(BaseDAO):
    """Data Access Object for User operations"""
    
    def authenticate(self, username, password):
        """Authenticate user"""
        try:
            query = "SELECT * FROM users WHERE username = ? AND password = ? AND status = 'Active'"
            return self.db.fetch_one(query, (username, password))
        except Exception as e:
            print(f"Authentication error: {e}")
            return None
    
    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            query = "SELECT * FROM users WHERE username = ?"
            return self.db.fetch_one(query, (username,))
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_last_login(self, user_id):
        """Update user's last login time"""
        try:
            data = {'last_login': datetime.datetime.now().isoformat()}
            self.db.update('users', data, 'id = ?', [user_id])
        except Exception as e:
            print(f"Error updating last login: {e}")
    
    def get_all_users(self):
        """Get all users"""
        try:
            return self.db.fetch_all("SELECT * FROM users ORDER BY id")
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def create_user(self, user_data):
        """Create a new user"""
        try:
            user_data['created_at'] = datetime.datetime.now().isoformat()
            return self.db.insert('users', user_data)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def update_user(self, user_id, user_data):
        """Update user"""
        try:
            user_data['updated_at'] = datetime.datetime.now().isoformat()
            self.db.update('users', user_data, 'id = ?', [user_id])
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, user_id):
        """Delete user"""
        try:
            self.db.delete('users', 'id = ?', [user_id])
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False


class BusDAO(BaseDAO):
    """Data Access Object for Bus operations"""
    
    def get_all_buses(self, filters=None):
        """Get all buses with optional filters"""
        try:
            query = '''
                SELECT b.*, 
                       i.policy_number, i.provider, i.coverage_amount, 
                       i.premium_amount, i.start_date, i.expiry_date,
                       i.status as insurance_status
                FROM buses b
                LEFT JOIN insurance i ON b.id = i.bus_id AND i.status = 'Active'
                WHERE 1=1
            '''
            params = []
            
            if filters:
                if filters.get('status') and filters['status'] != 'All':
                    query += " AND b.status = ?"
                    params.append(filters['status'])
                
                if filters.get('search'):
                    query += " AND (b.registration_number LIKE ? OR b.bus_number LIKE ? OR b.model LIKE ?)"
                    search_term = f"%{filters['search']}%"
                    params.extend([search_term, search_term, search_term])
            
            query += " ORDER BY b.id DESC"
            return self.db.fetch_all(query, params)
        except Exception as e:
            print(f"Error getting buses: {e}")
            return []
    
    def get_bus_by_id(self, bus_id):
        """Get bus by ID"""
        try:
            query = '''
                SELECT b.*, 
                       i.policy_number, i.provider, i.coverage_amount, 
                       i.premium_amount, i.start_date, i.expiry_date,
                       i.status as insurance_status
                FROM buses b
                LEFT JOIN insurance i ON b.id = i.bus_id AND i.status = 'Active'
                WHERE b.id = ?
            '''
            return self.db.fetch_one(query, (bus_id,))
        except Exception as e:
            print(f"Error getting bus: {e}")
            return None
    
    def add_bus(self, bus_data, insurance_data=None):
        """Add new bus with optional insurance"""
        try:
            bus_id = self.db.insert('buses', bus_data)
            
            if insurance_data and bus_id:
                insurance_data['bus_id'] = bus_id
                self.db.insert('insurance', insurance_data)
                
            self.log_activity('CREATE', 'Bus Management', f"Added bus: {bus_data.get('registration_number')}")
            return bus_id
        except Exception as e:
            print(f"Error adding bus: {e}")
            return None
    
    def update_bus(self, bus_id, bus_data, insurance_data=None):
        """Update bus and insurance information"""
        try:
            self.db.update('buses', bus_data, 'id = ?', [bus_id])
            
            if insurance_data:
                existing = self.db.fetch_one('SELECT id FROM insurance WHERE bus_id = ? AND status = "Active"', (bus_id,))
                if existing:
                    self.db.update('insurance', insurance_data, 'bus_id = ? AND status = "Active"', [bus_id])
                else:
                    insurance_data['bus_id'] = bus_id
                    self.db.insert('insurance', insurance_data)
            
            self.log_activity('UPDATE', 'Bus Management', f"Updated bus ID: {bus_id}")
            return True
        except Exception as e:
            print(f"Error updating bus: {e}")
            return False
    
    def delete_bus(self, bus_id):
        """Delete bus"""
        try:
            bus = self.get_bus_by_id(bus_id)
            self.db.delete('buses', 'id = ?', [bus_id])
            
            if bus:
                self.log_activity('DELETE', 'Bus Management', f"Deleted bus: {bus.get('registration_number')}")
            return True
        except Exception as e:
            print(f"Error deleting bus: {e}")
            return False
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard"""
        stats = {
            'total_buses': 0,
            'active_drivers': 0,
            'total_schools': 0,
            'active_contracts': 0
        }
        
        try:
            # Total buses
            result = self.db.fetch_one("SELECT COUNT(*) as count FROM buses")
            stats['total_buses'] = result['count'] if result else 0
            
            # Active drivers
            result = self.db.fetch_one("SELECT COUNT(*) as count FROM drivers WHERE status = 'Active'")
            stats['active_drivers'] = result['count'] if result else 0
            
            # Total schools
            result = self.db.fetch_one("SELECT COUNT(*) as count FROM schools")
            stats['total_schools'] = result['count'] if result else 0
            
            # Active contracts
            result = self.db.fetch_one("SELECT COUNT(*) as count FROM schools WHERE contract_status = 'Active'")
            stats['active_contracts'] = result['count'] if result else 0
            
        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
        
        return stats
    
    def get_recent_activities(self, limit=5):
        """Get recent activities"""
        try:
            # Check if table exists
            tables = self.db.fetch_all("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_logs'")
            if not tables:
                return []
                
            query = '''
                SELECT timestamp, username, action, module, details 
                FROM activity_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            '''
            return self.db.fetch_all(query, (limit,))
        except Exception as e:
            print(f"Error getting activities: {e}")
            return []