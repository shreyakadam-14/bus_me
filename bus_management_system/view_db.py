# web_viewer.py
import sqlite3
import http.server
import socketserver
import json
from urllib.parse import parse_qs

PORT = 8000

class DatabaseHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Database Viewer</title>
                <style>
                    body { font-family: Arial; margin: 20px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                    tr:nth-child(even) { background-color: #f2f2f2; }
                    .table-selector { margin-bottom: 20px; }
                    select, button { padding: 10px; font-size: 16px; }
                </style>
                <script>
                    function loadTable() {
                        var table = document.getElementById('tableSelect').value;
                        fetch('/data?table=' + table)
                            .then(response => response.json())
                            .then(data => {
                                var html = '<h2>Table: ' + table + '</h2>';
                                html += '<table><tr>';
                                if (data.columns) {
                                    data.columns.forEach(col => {
                                        html += '<th>' + col + '</th>';
                                    });
                                    html += '</tr>';
                                    
                                    data.rows.forEach(row => {
                                        html += '<tr>';
                                        row.forEach(cell => {
                                            html += '<td>' + (cell || '') + '</td>';
                                        });
                                        html += '</tr>';
                                    });
                                    html += '</table>';
                                }
                                document.getElementById('data').innerHTML = html;
                            });
                    }
                </script>
            </head>
            <body>
                <h1>Database Viewer</h1>
                <div class="table-selector">
                    <select id="tableSelect">
                        <option value="users">Users</option>
                        <option value="buses">Buses</option>
                        <option value="drivers">Drivers</option>
                        <option value="schools">Schools</option>
                        <option value="insurance">Insurance</option>
                        <option value="transactions">Transactions</option>
                    </select>
                    <button onclick="loadTable()">Load Table</button>
                </div>
                <div id="data"></div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path.startswith('/data'):
            query = parse_qs(self.path.split('?')[1] if '?' in self.path else '')
            table = query.get('table', [''])[0]
            
            conn = sqlite3.connect('data/bus_management.db')
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                cursor.execute(f"SELECT * FROM {table} LIMIT 100")
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                data = {
                    'columns': columns,
                    'rows': [[str(cell) for cell in row] for row in rows]
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            
            conn.close()
        else:
            super().do_GET()

print(f"Starting web viewer at http://localhost:{PORT}")
print("Press Ctrl+C to stop")
with socketserver.TCPServer(("", PORT), DatabaseHandler) as httpd:
    httpd.serve_forever()