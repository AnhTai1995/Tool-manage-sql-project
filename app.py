from flask import Flask, render_template, request, jsonify
import os
import json

app = Flask(__name__)

# Path to the file where SQL entries are saved
SQL_FILE = 'database/sql_list_db.txt'

# Load SQL entries from file
def load_sql_entries():
    if os.path.exists(SQL_FILE):
        with open(SQL_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Save SQL entries to file
def save_sql_entries(sql_entries):
    with open(SQL_FILE, 'w') as file:
        json.dump(sql_entries, file)

# Initialize SQL entries
sql_entries = load_sql_entries()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_sql', methods=['POST'])
def add_sql():
    data = request.json
    new_entry = {
        'id': max([entry['id'] for entry in sql_entries], default=0) + 1,
        'title': data['title'],
        'code': data['code'],
        'keywords': data['keywords']
    }
    sql_entries.append(new_entry)
    save_sql_entries(sql_entries)
    return jsonify({'success': True, 'entry': new_entry})

@app.route('/get_sql', methods=['GET'])
def get_sql():
    return jsonify({'codes': sql_entries})

# Endpoint to fetch a specific SQL entry by ID
@app.route('/get_sql_entry', methods=['GET'])
def get_sql_entry():
    sql_id = request.args.get('id', type=int)
    sql_entry = next((entry for entry in sql_entries if entry['id'] == sql_id), None)
    if sql_entry:
        return jsonify(sql_entry)
    else:
        return jsonify({'error': 'SQL entry not found'}), 404

@app.route('/update_sql', methods=['POST'])
def update_sql():
    data = request.json
    for entry in sql_entries:
        if entry['id'] == int(data['id']):
            entry['title'] = data['title']
            entry['code'] = data['code']
            entry['keywords'] = data['keywords']
            save_sql_entries(sql_entries)
            return jsonify({'success': True, 'entry': entry})
    return jsonify({'success': False, 'message': 'Entry not found'})

@app.route('/delete_sql', methods=['POST'])
def delete_sql():
    data = request.json
    global sql_entries
    sql_entries = [entry for entry in sql_entries if entry['id'] != data['id']]
    save_sql_entries(sql_entries)
    return jsonify({'success': True})

@app.route('/search_sql', methods=['GET'])
def search_sql_entries():
    query = request.args.get('query', '').lower()
    entries = load_sql_entries()
    filtered_entries = [
        e for e in entries
        if query in e['title'].lower() or query in e['keywords'].lower()
    ]
    return jsonify(filtered_entries)

if __name__ == '__main__':
    app.run(debug=True)
