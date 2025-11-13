from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración para la base de datos
DB_HOST = 'db-calses.cjuwydxejd04.us-east-1.rds.amazonaws.com'  
DB_PORT = 3306         
DB_USER = 'admin'
DB_PASSWORD = 'cristhian3738'
DB_NAME = 'register_db'  

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a la base de datos", 500
    cursor = conn.cursor(dictionary=True)
    
    # Obtener parámetros de búsqueda
    query = request.args.get('q')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    # Construir consulta SQL con filtros
    sql = "SELECT * FROM items WHERE 1=1"
    params = []
    
    if query:
        sql += " AND name LIKE %s"
        params.append('%' + query + '%')
    
    if fecha_inicio:
        sql += " AND DATE(created_at) >= %s"
        params.append(fecha_inicio)
    
    if fecha_fin:
        sql += " AND DATE(created_at) <= %s"
        params.append(fecha_fin)
    
    sql += " ORDER BY created_at DESC"
    
    cursor.execute(sql, params)
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    conn = get_db_connection()
    if not conn:
        return "Error de conexión", 500
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    if not conn:
        return "Error de conexión", 500
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        cursor.execute("UPDATE items SET name = %s WHERE id = %s", (name, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM items WHERE id = %s", (id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('form.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    if not conn:
        return "Error de conexión", 500
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Ejecutar servidor local en Flask
    app.run(host='127.0.0.1', port=5000, debug=True)

