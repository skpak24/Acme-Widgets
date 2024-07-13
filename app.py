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
    if 'db' not in g:
        g.db = sqlite3.connect(database)
        g.db.execute('PRAGMA foreign_keys = ON;')
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# make jobs table if not exists
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jha (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                jobTitle TEXT 
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                jhaId      INTEGER NOT NULL,
                FOREIGN KEY (jhaId)
                REFERENCES jha (id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hazards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                stepId    INTEGER NOT NULL,
                FOREIGN KEY (stepId)
                REFERENCES steps (id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mitigations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                hazardId   INTEGER NOT NULL,
                FOREIGN KEY (hazardId)
                REFERENCES hazards (id) ON DELETE CASCADE
            )
        ''')
        db.commit()

init_db()

# get all jha
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
        SELECT jha.id, jha.name, jha.jobTitle, steps.id, steps.description, hazards.id, hazards.description, mitigations.id, mitigations.description
        FROM jha
        LEFT JOIN steps ON jha.id = steps.jhaId
        LEFT JOIN hazards ON steps.id = hazards.stepId
        LEFT JOIN mitigations ON hazards.id = mitigations.hazardId
        ORDER BY jha.id, steps.id, hazards.id, mitigations.id
        ''')
        rows = cursor.fetchall()

        #fix format
        jobs = {}
        for row in rows:
            jha_id = row[0]
            if jha_id not in jobs: 
                jobs[jha_id] = {
                    'id': jha_id,
                    'name': row[1],
                    'jobTitle': row[2],
                    'steps': []
                }

            step_id = row[3]
            if step_id:
                steps = {step['id'] for step in jobs[jha_id]['steps']}
                if step_id not in steps:
                    jobs[jha_id]['steps'].append({
                        'id': step_id,
                        'stepDesc': row[4],
                        'haz': []
                    })

                hazard_id = row[5]
                if hazard_id:
                    hazards = {hazard['id'] for hazard in jobs[jha_id]['steps'][-1]['haz']}
                    if hazard_id not in hazards:
                        jobs[jha_id]['steps'][-1]['haz'].append({
                            'id': hazard_id,
                            'hazDesc': row[6],
                            'mit': []
                        })

                    mitigation_id = row[7]
                    if mitigation_id:
                        mitigations = {mitigation['id'] for mitigation in jobs[jha_id]['steps'][-1]['haz'][-1]['mit']}
                        if mitigation_id not in mitigations:
                            jobs[jha_id]['steps'][-1]['haz'][-1]['mit'].append({
                                'id': mitigation_id,
                                'mitDesc': row[8]
                            })

        return jsonify(list(jobs.values())), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500


# add new jha, DATABASE RELATED
@app.route('/api/jobs', methods=['POST'])
def create_job():
    try:
        new_job = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO jha (name, jobTitle) VALUES (?, ?)',
                       (new_job['name'], new_job['jobTitle']))
        jha_id = cursor.lastrowid
            
        for step in new_job['steps']:
            cursor.execute('INSERT INTO steps (jhaId, description) VALUES (?, ?)',
                            (jha_id, step['stepDesc']))
            step_id = cursor.lastrowid
            
            for hazard in step['haz']:
                cursor.execute('INSERT INTO hazards (stepId, description) VALUES (?, ?)',
                                (step_id, hazard['hazDesc']))
                hazard_id = cursor.lastrowid
                
                for mitigation in hazard['mit']:
                    cursor.execute('INSERT INTO mitigations (hazardId, description) VALUES (?, ?)',
                                    (hazard_id, mitigation))
                    
        db.commit()
        return jsonify({'message': 'Job created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# update jha
@app.route('/api/jobs/<int:id>', methods=['PUT'])
def update_job(id):
    try:
        updated_job = request.json
        db = get_db()
        cursor = db.cursor()
        cursor.execute('UPDATE jha SET name=?, jobTitle=? WHERE id=?',
                       (updated_job['name'], updated_job['jobTitle'], id))
        cursor.execute('DELETE FROM steps WHERE jhaId=?', (id,))
        
        for step in updated_job['steps']:
            cursor.execute('INSERT INTO steps (jhaId, description) VALUES (?, ?)',
                           (id, step['stepDesc']))
            step_id = cursor.lastrowid

            for hazard in step['haz']:
                cursor.execute('INSERT INTO hazards (stepId, description) VALUES (?, ?)',
                               (step_id, hazard['hazDesc']))
                hazard_id = cursor.lastrowid

                for mitigation in hazard['mit']:
                    cursor.execute('INSERT INTO mitigations (hazardId, description) VALUES (?, ?)',
                                   (hazard_id, mitigation))

        db.commit()
        return jsonify({'message': f'Job {id} updated successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# delete jha
@app.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM jha WHERE id=?', (id,))
        db.commit()
        return jsonify({'message': f'Job {id} and related data deleted successfully'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)