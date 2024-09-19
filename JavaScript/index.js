// app.js

const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const PORT = 3000;

const uri = "/v1/items";

// Configuración de la conexión a la base de datos MySQL
const db = mysql.createConnection({
    host: 'localhost', 
    user: 'root', 
    password: '', 
    database: 'exposicionis2', 
});

// Conexión a la base de datos
db.connect((err) => {
    if (err) {
        console.error('Error al conectar a la base de datos MySQL:', err);
    } else {
        console.log('Conexión exitosa a la base de datos MySQL');
    }
});

// Middleware para analizar datos JSON
app.use(bodyParser.json());

// Rutas

// Obtener todos los elementos
app.get(uri, (req, res) => {
    const query = 'SELECT * FROM items';
    db.query(query, (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al obtener los elementos' });
        } else {
            res.json(results);
        }
    });
});

// Obtener un elemento específico por su ID
app.get(`${uri}/:id`, (req, res) => {
    const itemId = req.params.id;
    const query = 'SELECT * FROM items WHERE id = ?';
    db.query(query, [itemId], (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al obtener el elemento' });
        } else if (results.length === 0) {
            res.status(404).json({ error: 'Elemento no encontrado' });
        } else {
            res.json(results[0]);
        }
    });
});

// Crear un nuevo elemento
app.post(`${uri}`, (req, res) => {
    const newItem = req.body;
    const query = 'INSERT INTO items (name, description) VALUES (?, ?)';
    db.query(query, [newItem.name, newItem.description], (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Error al crear el elemento' });
        } else {
            newItem.id = result.insertId;
            res.status(201).json(newItem);
        }
    });
});

// Actualizar un elemento existente
app.put(`${uri}/:id`, (req, res) => {
    const itemId = req.params.id;
    const updatedItem = req.body;
    const query = 'UPDATE items SET name = ?, description = ? WHERE id = ?';
    db.query(query, [updatedItem.name, updatedItem.description, itemId], (err) => {
        if (err) {
            res.status(500).json({ error: 'Error al actualizar el elemento' });
        } else {
            res.json(updatedItem);
        }
    });
});

// Eliminar un elemento
app.delete(`${uri}/:id`, (req, res) => {
    const itemId = req.params.id;
    const query = 'DELETE FROM items WHERE id = ?';
    db.query(query, [itemId], (err, result) => {
        if (err) {
            res.status(500).json({ error: 'Error al eliminar el elemento' });
        } else if (result.affectedRows === 0) {
            res.status(404).json({ error: 'Elemento no encontrado' });
        }
        else {
            res.json({ message: 'Elemento eliminado correctamente' });
        }
    });
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Servidor iniciado en http://localhost:${PORT}`);
});