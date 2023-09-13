from flask import Flask, url_for, render_template, request, redirect
import sqlite3

app = Flask('__name__')

def create_database():
    conexion = sqlite3.connect('task.db')
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tarea(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tareas TEXT NOT NULL)""")
    conexion.commit()
    conexion.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'tareas' in request.form:
        with app.app_context():
            conexion = sqlite3.connect('task.db')
            cursor = conexion.cursor()
            tareas = request.form.get('tareas')
            cursor.execute("INSERT INTO tarea (tareas) VALUES (?)", (tareas,))
            conexion.commit()
            conexion.close()

        return redirect(url_for('index')) 

    with app.app_context():
        conexion = sqlite3.connect('task.db')
        cursor = conexion.cursor()
        datos = cursor.execute("SELECT * FROM tarea").fetchall()
        conexion.commit()
        conexion.close()

    return render_template('tasks.html',datos=datos)    

@app.route('/delete/<int:id>', methods=['GET'])    
def deleted(id):
    with app.app_context():
        conexion = sqlite3.connect('task.db')
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM tarea WHERE id = ?", (id,))
        conexion.commit()
        conexion.close()

    return redirect(url_for('index'))    

if __name__ == '__main__':
    create_database()
    app.run('localhost', debug=True, port=8000)