from flask import Blueprint, jsonify, request
from services.sensor_service import SensorService

sensores_bp = Blueprint("sensores", __name__)
sensor_service = SensorService()

@sensores_bp.post("/sensores")
def criar():
    data = request.json
    sensor = sensor_service.criar_sensor(data)
    return jsonify(sensor.to_dict()), 201

@sensores_bp.get("/sensores")
def listar():
    sensores = sensor_service.listar_sensores()
    return jsonify([s.to_dict() for s in sensores])

@sensores_bp.get("/sensores/<int:sensor_id>")
def obter(sensor_id):
    sensor = sensor_service.obter_sensor_por_id(sensor_id)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.delete("/sensores/<int:sensor_id>")
def remover(sensor_id):
    sucesso = sensor_service.remover_sensor(sensor_id)
    if sucesso:
        return jsonify({"message": "Sensor removido com sucesso"})
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.put("/sensores/<int:sensor_id>")
def atualizar(sensor_id):
    data = request.json
    sensor = sensor_service.atualizar_sensor(sensor_id, data)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404
