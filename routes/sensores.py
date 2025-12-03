from flask import Blueprint, jsonify, request
from services.sensor_service import SensorService

sensores_bp = Blueprint("sensores", __name__)
sensor_service = SensorService()

@sensores_bp.post("/dispositivos/<dispositivo_uuid>/sensores")
def criar(dispositivo_uuid):
    data = request.json
    sensor = sensor_service.criar_sensor(dispositivo_uuid, data)
    return jsonify(sensor.to_dict()), 201

@sensores_bp.get("/dispositivos/<dispositivo_uuid>/sensores")
def listar(dispositivo_uuid):
    sensores = sensor_service.listar_sensores(dispositivo_uuid)
    return jsonify([s.to_dict() for s in sensores])

@sensores_bp.get("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>")
def obter(dispositivo_uuid, sensor_id):
    sensor = sensor_service.obter_sensor_por_id(dispositivo_uuid, sensor_id)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.delete("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>")
def remover(dispositivo_uuid, sensor_id):
    sucesso = sensor_service.remover_sensor(dispositivo_uuid, sensor_id)
    if sucesso:
        return "", 204
    return jsonify({"error": "Sensor não encontrado"}), 404

@sensores_bp.put("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>")
def atualizar(dispositivo_uuid, sensor_id):
    data = request.json
    sensor = sensor_service.atualizar_sensor(dispositivo_uuid, sensor_id, data)
    if sensor:
        return jsonify(sensor.to_dict())
    return jsonify({"error": "Sensor não encontrado"}), 404
