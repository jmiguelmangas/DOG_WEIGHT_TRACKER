import json
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Blueprint, jsonify, request

bp = Blueprint('readData', __name__)

@bp.route('/data', methods=['GET'])
def leer_registros():
    nombres = request.args.getlist('nombre')
    
    archivo = 'data.json'
    try:
        with open(archivo, 'r') as f:
            datos = json.load(f)
        return jsonify(datos["entities"]), 200
    except FileNotFoundError:
        return jsonify([]), 200

    if not nombres:
        return jsonify(datos["entities"]), 200
    
    resultados = [entidad for entidad in datos["entities"] if entidad["nombre"] in nombres]
    return jsonify(resultados), 200

@bp.route('/graph', methods=['GET'])
def crear_grafica():
    nombres = request.args.getlist('nombre')
    
    archivo = 'data.json'
    try:
        with open(archivo, 'r') as f:
            datos = json.load(f)
    except FileNotFoundError:
        return jsonify({"message": "No hay datos para graficar"}), 404
    
    plt.figure(figsize=(10, 5))
    
    for entidad in datos["entities"]:
        if entidad["nombre"] in nombres or not nombres:
            fechas = [datetime.strptime(peso['fecha'], "%Y-%m-%d") for peso in entidad["pesos"]]
            pesos = [peso['peso'] for peso in entidad["pesos"]]
            plt.plot(fechas, pesos, label=f'Peso {entidad["nombre"]}', marker='o')
    
    if not plt.gca().has_data():
        return jsonify({"message": "No hay datos para graficar"}), 404
    
    plt.xlabel('Fecha')
    plt.ylabel('Peso (kg)')
    plt.title('Registro de peso')
    plt.legend()
    plt.grid(True)
    plt.gcf().autofmt_xdate()  # Rotar etiquetas de fecha

    plt.savefig('graph.png')
    return jsonify({"message": "Gráfica creada exitosamente"}), 200

def init_app(app):
    app.register_blueprint(bp)
