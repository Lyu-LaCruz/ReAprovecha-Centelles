from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/productos.json'


def cargar_productos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def guardar_producto(producto):
    productos = cargar_productos()
    productos.append(producto)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(productos, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    productos = cargar_productos()
    productos = sorted(productos, key=lambda x: x['hora'], reverse=True)
    return render_template('index.html', productos=productos)


@app.route('/publicar', methods=['POST'])
def publicar():
    nombre = request.form['nombre']
    negocio = request.form['negocio']
    descripcion = request.form['descripcion']
    hora = datetime.now().strftime('%Y-%m-%d %H:%M')
    producto = {'nombre': nombre, 'negocio': negocio, 'descripcion': descripcion, 'hora': hora}
    guardar_producto(producto)
    return redirect('/')


@app.route('/productos')
def productos():
    productos = cargar_productos()
    return render_template('productos.html', productos=productos)


@app.route('/perfil')
def perfil():
    return render_template('perfil.html')


@app.route('/static/js/<path:filename>')
def custom_static(filename):
    return send_from_directory('static/js', filename)


if __name__ == '__main__':
    app.run(debug=True)
