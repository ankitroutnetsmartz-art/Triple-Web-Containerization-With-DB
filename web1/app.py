from flask import Flask, render_template, request
import mariadb
import socket

app = Flask(__name__)
node_id = socket.gethostname()

def get_db():
    return mariadb.connect(host="db", user="user", password="password", database="app_db")

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', site="ALPHA", node=node_id)

@app.route('/admin')
def admin():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, created_at FROM site_logins ORDER BY created_at DESC LIMIT 50")
        entries = cur.fetchall()
        conn.close()
        return render_template('admin.html', site="ALPHA", node=node_id, entries=entries)
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
