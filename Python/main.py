from flask import Flask, request, jsonify 
import mysql.connector 
from mysql.connector import Error

app = Flask(__name__)
PORT = 3000

# Configuración de la conexión a la base de datos MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='exposicionis2'
        )
        if connection.is_connected():
            print('Conexión exitosa a la base de datos MySQL')
    except Error as e:
        print(f'Error al conectar a la base de datos MySQL: {e}')
    return connection

# Obtener todos los elementos
@app.route('/items', methods=['GET']) 
def get_items():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True) # Se crea un cursor con el parámetro dictionary=True para obtener los resultados como diccionarios
    cursor.execute('SELECT * FROM items') # Se ejecuta la consulta SQL para obtener todos los elementos
    results = cursor.fetchall()  # Se obtienen todos los elementos
    cursor.close() 
    connection.close()
    return jsonify(results)

# Obtener un elemento específico por su ID
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items WHERE id = %s', (id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(results) == 0:
        return jsonify({'error': 'Elemento no encontrado'}), 404
    return jsonify(results[0])

# Crear un nuevo elemento
@app.route('/items', methods=['POST'])
def create_item():
    new_item = request.json
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (new_item['name'], new_item['description']))
    connection.commit() 
    new_item['id'] = cursor.lastrowid
    cursor.close()
    connection.close()
    return jsonify(new_item), 201

# Actualizar un elemento existente
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    updated_item = request.json
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s', (updated_item['name'], updated_item['description'], id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(updated_item)

# Eliminar un elemento
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM items WHERE id = %s', (id,))
    connection.commit()
    if cursor.rowcount == 0:
        cursor.close()
        connection.close()
        return jsonify({'error': 'Elemento no encontrado'}), 404
    cursor.close()
    connection.close()
    return jsonify({'message': 'Elemento eliminado correctamente'})

# Iniciar el servidor
if __name__ == '__main__':
    app.run(port=PORT)

# python main.py
# curl http://localhost:3000/items
# method = ['GET', 'POST', 'PUT', 'DELETE']