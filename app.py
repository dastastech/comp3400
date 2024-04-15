from flask import Flask, jsonify, request
import mariadb
import sys

#imporst db access config
from config import DATABASE_CONFIG


app = Flask(__name__)

try:
        conn = mariadb.connect(**DATABASE_CONFIG)
except mariadb.Error as e:
        print(f"Error  on connection: {e}")
        sys.exit(1)

cursor = conn.cursor()


@app.route('/api/hello', methods=['GET'])
def hello_world():
        return jsonify({'message': '¡Hola, mundo con Flask!'})

@app.route('/api/misdatos/', methods=['GET'])
def mis_datos():
        return jsonify({'datos': '** SU NOMBRE ** !'})


@app.route('/api/get_users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM Usuarios")
    users = cursor.fetchall()
    # Convertir los resultados en un formato más amigable o devolverlos directamente
    return jsonify(users)

@app.route('/api/get_user/<int:id>', methods=['GET'])
def get_user(id):
    if (id == 0):
           return jsonify({"error":"Invalid ID"}), 404
    else:
        cursor.execute("SELECT * FROM Usuarios where id_usuario = ?", (id,))
        user = cursor.fetchone()
        # Convertir los resultados en un formato más amigable o devolverlos directamente
        return jsonify(user)

@app.route('/api/new_user', methods=['POST'])
def new_user():
        datos = request.json
        name = datos.get('nombre')
        lastname = datos.get('apellido')
        email = datos.get('email')
        pwd = datos.get('contrasena')
        role = datos.get('rol')
        
        strQry = 'insert into Usuarios '
        strQry += "(nombre, apellido, email, contrasena, rol) "
        strQry += f"values ('{name}','{lastname}','{email}','{pwd}','{role}')"

        cursor.execute(strQry)        

        response = {"message":"Record inserted"}
    
        return jsonify(response) , 200


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)

