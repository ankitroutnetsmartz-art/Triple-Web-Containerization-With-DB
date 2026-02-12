from flask import Flask, render_template, request, redirect
import mariadb
import socket

app = Flask(__name__)
node_id = socket.gethostname()

def get_db():
    return mariadb.connect(host="db", user="user", password="password", database="app_db")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('pass')
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO site_logins (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            # After POST, redirect to prevent form re-submission
            return redirect('/')
        except Exception as e:
            return f"Database Error: {str(e)}"
    
    return render_template('index.html', site="BETA", node=node_id)

@app.route('/admin')
def admin():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id, username, created_at FROM site_logins ORDER BY created_at DESC")
        entries = cur.fetchall()
        conn.close()
        return render_template('admin.html', site="BETA", node=node_id, entries=entries)
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
