from flask import Blueprint, jsonify, request
from services.alerta_service import AlertaService

alertas_bp = Blueprint("alertas", __name__)
alerta_service = AlertaService()

@alertas_bp.post("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/alertas")
def criar(dispositivo_uuid, sensor_id):
    data = request.json
    alerta = alerta_service.criar_alerta(dispositivo_uuid, sensor_id, data)
    if alerta:
        return jsonify(alerta.to_dict()), 201
    return jsonify({"error": "Alerta não criado"}), 400

@alertas_bp.get("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/alertas")
def listar(dispositivo_uuid, sensor_id):
    alertas = alerta_service.listar_alertas(dispositivo_uuid, sensor_id)
    return jsonify([a.to_dict() for a in alertas])

@alertas_bp.get("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/alertas/<int:alerta_id>")
def obter(dispositivo_uuid, sensor_id, alerta_id):
    alerta = alerta_service.obter_alerta_por_id(dispositivo_uuid, sensor_id, alerta_id)
    if alerta:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado"}), 404

@alertas_bp.patch("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/alertas/<int:alerta_id>")
def atualizar_status(dispositivo_uuid, sensor_id, alerta_id):
    data = request.json
    resolvido = data.get("resolvido")
    if resolvido is None:
        return jsonify({"error": "Campo 'resolvido' é obrigatório"}), 400

    alerta = alerta_service.atualizar_status_alerta(dispositivo_uuid, sensor_id, alerta_id, resolvido)
    if alerta:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado"}), 404

@alertas_bp.delete("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/alertas/<int:alerta_id>")
def remover(dispositivo_uuid, sensor_id, alerta_id):
    sucesso = alerta_service.remover_alerta(dispositivo_uuid, sensor_id, alerta_id)
    if sucesso:
        return "", 204
    return jsonify({"error": "Alerta não encontrado"}), 404
