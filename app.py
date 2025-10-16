from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from database import init_db

app = Flask(__name__, static_folder="static")
CORS(app)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

init_db()

@app.route('/entities', methods=['GET'])
def get_all():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(row) for row in books])

@app.route('/entities/<int:id>', methods=['GET'])
def get_one(id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (id,)).fetchone()
    conn.close()
    if book is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dict(book))

@app.route('/entities', methods=['POST'])
def create():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO books (title, pages, author, year) VALUES (?, ?, ?, ?)',
                (data.get('title'), data.get('pages'), data.get('author'), data.get('year')))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({'id': new_id}), 201

@app.route('/entities/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE books SET title=?, pages=?, author=?, year=? WHERE id=?',
                (data.get('title'), data.get('pages'), data.get('author'), data.get('year'), id))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.close()
    return jsonify({'updated': True})

@app.route('/entities/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM books WHERE id=?', (id,))
    conn.commit()
    if cur.rowcount == 0:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.close()
    return jsonify({'deleted': True})

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)