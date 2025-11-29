from flask import Blueprint, jsonify, request
from services.sensor_service import criar_sensor, listar_sensores, obter_sensor_por_id, remover_sensor, atualizar_sensor

sensores_bp = Blueprint("sensores", __name__)

@sensores_bp.post("/sensores")
def criar():
    data = request.json
    sensor = criar_sensor(data)
    return jsonify(sensor.to_dict()), 201

@sensores_bp.get("/sensores")
def listar():
    sensores = listar_sensores()
    return jsonify([s.to_dict() for s in sensores])

@sensores_bp.get("/sensores/<int:sensor_id>")
def obter(sensor_id):
    sensor = obter_sensor_por_id(sensor_id)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.delete("/sensor/<int:sensor_id>/remove")
def remover(sensor_id):
    sucesso = remover_sensor(sensor_id)
    if sucesso:
        return jsonify({"message": "Sensor removido com sucesso"})
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.put("/sensor/<int:sensor_id>/update")
def atualizar(sensor_id):
    data = request.json
    sensor = atualizar_sensor(sensor_id, data)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404

