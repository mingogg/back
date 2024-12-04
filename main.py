from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2 # Para conectar con Postgres


# Se instancia la clase Flask en la variable [app]
# Para tener todos los métodos dentro de una sola variable
app = Flask(__name__)
CORS(app)

# Connect to the database
conn = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "postgres",
    port = "5432"
)

# Crear una tarea ruta1
@app.route("/crear", methods = ["POST"])

def crear_tarea():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")

    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    cur.close()
    return jsonify(
        {"message":"Tarea " + title + " creada exitosamente"}
    )

# Listar todas las tareas ruta2
@app.route("/listado", methods = ["GET"])

def listar_tareas():
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, isdone FROM tasks order by 1 desc")
    rows = cur.fetchall()
    cur.close()
    
    tareas = []
    for row in rows:
        tareas.append({
            "id":row[0],
            "title":row[1],
            "description":row[2],
            "isdone":row[3],
        })

    return jsonify(tareas)

# Listar la tarea por ID ruta3
@app.route("/tarea/<int:tasksid>", methods = ["GET"])
def obtener_tarea(tasksid):
    cur = conn.cursor()
    cur.execute("SELECT id, title, description, isdone FROM tasks where id = %s order by 1 desc", (tasksid, ))
    
    task = cur.fetchone()
    
    if task:
        return jsonify(
            {
                "tasksid":task[0],
                "title":task[1],
                "description":task[2],
                "isdone":task[3],
            }
        )
    else:
        return jsonify({"error":"Tarea no encontrada"}), 404

# Modificar la tarea ruta4
@app.route("/modificar/<int:tasksid>", methods = ["PUT"])
def modificar_tarea(tasksid):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET title = %s, description = %s WHERE id = %s", (title, description, tasksid, ))
    conn.commit()
    cur.close()
    return jsonify({"mensaje":"tarea actualizada correctamente"})

# Eliminar una tarea ruta5
@app.route("/eliminar/<int:tasksid>", methods = ["DELETE"])
def eliminar_tarea(tasksid):

    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (tasksid, ))
    conn.commit()
    cur.close()
    return jsonify({"mensaje":"tarea eliminada correctamente"})

# Marcar una tarea como completada ruta6
@app.route("/estado/<tasksid>", methods = ["PATCH"])
def modificar_estado(tasksid):
    data = request.get_json()
    isdone = data.get("isdone")
    
    if isdone is None:
        query = "UPDATE tasks SET isdone = NULL WHERE id = %s"
        params = (tasksid, )
    else:
        query = "UPDATE tasks SET isdone = %s WHERE id = %s"
        params =  (isdone, tasksid)
    
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    return jsonify({"mensaje":"cambio el estado de la tarea"})

if __name__ == "__main__":
    app.run(debug = True)