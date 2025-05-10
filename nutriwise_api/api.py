from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'nutriwise_secret_key'

# ---------- DB Helper ----------
def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.join(base_dir, 'database')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'users.db')
    return sqlite3.connect(db_path)

# ---------- REGISTER ----------
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        conn = get_db()
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
        c.execute('INSERT INTO users VALUES (?, ?)', (data['username'], data['password']))
        conn.commit()
        return jsonify({"message": "Registration successful!"})
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 409
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (data['username'], data['password']))
        user = c.fetchone()
        if user:
            token = jwt.encode({
                'username': user[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

# ---------- SAVE USER PREFS ----------
@app.route('/save_preferences', methods=['POST'])
def save_preferences():
    try:
        data = request.get_json()
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                username TEXT PRIMARY KEY,
                age INTEGER,
                weight REAL,
                height REAL,
                activity TEXT,
                goal TEXT,
                diet TEXT,
                allergies TEXT
            )
        ''')
        c.execute('''REPLACE INTO preferences (username, age, weight, height, activity, goal, diet, allergies)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['username'], data['age'], data['weight'], data['height'],
                   data['activity'], data['goal'], data['diet'], data['allergies']))
        conn.commit()
        return jsonify({"message": "Preferences saved."})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

# ---------- GET USER PREFS ----------
@app.route('/get_preferences', methods=['GET'])
def get_preferences():
    try:
        username = request.args.get('username')
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM preferences WHERE username=?', (username,))
        row = c.fetchone()
        if row:
            return jsonify({
                "username": row[0],
                "age": row[1], "weight": row[2], "height": row[3],
                "activity": row[4], "goal": row[5], "diet": row[6], "allergies": row[7]
            })
        else:
            return jsonify({})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

# ---------- UPDATE PREFS ----------
@app.route('/update_preferences', methods=['PUT'])
def update_preferences():
    try:
        data = request.get_json()
        username = data.get('username')
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            UPDATE preferences SET
                age = ?, weight = ?, height = ?, activity = ?,
                goal = ?, diet = ?, allergies = ?
            WHERE username = ?
        ''', (data['age'], data['weight'], data['height'], data['activity'],
              data['goal'], data['diet'], data['allergies'], username))
        conn.commit()
        return jsonify({"message": "Preferences updated successfully."})
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    finally:
        try:
            conn.close()
        except:
            pass

# ---------- START ----------
if __name__ == '__main__':
    app.run(debug=True)
