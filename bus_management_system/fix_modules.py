# fix_modules.py
import os

def fix_imports_in_file(filename):
    """Fix imports in a module file"""
    if not os.path.exists(filename):
        print(f"✗ {filename} not found")
        return
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Check if QGridLayout is in imports
    if 'QGridLayout' not in content:
        # Add QGridLayout to the import list
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'from PyQt5.QtWidgets import (' in line:
                # Find the import block
                import_lines = []
                j = i
                while j < len(lines) and ')' not in lines[j]:
                    import_lines.append(lines[j])
                    j += 1
                if j < len(lines):
                    import_lines.append(lines[j])  # Add the closing line
                
                # Add QGridLayout to imports
                for k in range(len(import_lines)):
                    if 'QVBoxLayout' in import_lines[k]:
                        import_lines[k] = import_lines[k].replace('QVBoxLayout', 'QVBoxLayout, QGridLayout')
                        break
                
                # Replace the import block
                lines[i:j+1] = import_lines
                break
        
        new_content = '\n'.join(lines)
        
        with open(filename, 'w') as f:
            f.write(new_content)
        
        print(f"✓ Fixed imports in {filename}")
    else:
        print(f"✓ {filename} already has QGridLayout")

# List of module files to fix
module_files = [
    'modules/bus_management_db.py',
    'modules/driver_management_db.py',
    'modules/school_management_db.py',
    'modules/system_admin_db.py',
    'modules/system_settings_db.py',
    'modules/reports_dashboard_db.py'
]

print("Fixing module imports...")
for file in module_files:
    fix_imports_in_file(file)

print("\nDone! Now run: python main.py")