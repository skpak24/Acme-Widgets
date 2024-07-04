from flask import Flask, jsonify, request, g
from flask_cors import CORS
import sqlite3
import os
import json

app = Flask(__name__)

# allow requests between different ports
CORS(app)

# database file
database = os.path.join(os.path.dirname(__file__), 'jobs.db')

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:1993'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    return response

# SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Flask._database = sqlite3.connect(database)
    return db

# make jobs table if not exists
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                jobTitle TEXT,
                steps TEXT
            )
        ''')
        db.commit()

init_db()

# get all jha
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall()
        conn.close()

        #fix format
        formatted_jobs = []
        for job in jobs:
            formatted_jobs.append({
                'id': job[0],
                'name': job[1],
                'jobTitle': job[2],
                'steps': json.loads(job[3])
        })

        return jsonify(formatted_jobs), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


# add new jha
@app.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        new_job = request.json
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO jobs (name, jobTitle, steps) VALUES (?, ?, ?)',
                       (new_job['name'], new_job['jobTitle'], json.dumps(new_job['steps'])))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Job created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# update jha
@app.route('/api/jobs/<int:id>', methods=['PUT'])
def update_job(id):
    try:
        updated_job = request.json
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('UPDATE jobs SET name=?, jobTitle=?, steps=? WHERE id=?',
                       (updated_job['name'], updated_job['jobTitle'], json.dumps(updated_job['steps']), id))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Job {id} updated successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    

# delete jha
@app.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM jobs WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Job {id} deleted successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)