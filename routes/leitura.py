from flask import Blueprint, jsonify, request
from services.leitura_service import LeituraService

leituras_bp = Blueprint("leituras", __name__)
leitura_service = LeituraService()

@leituras_bp.post("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/leituras")
def criar(dispositivo_uuid, sensor_id):
    data = request.json
    leitura = leitura_service.registrar_leitura(dispositivo_uuid, sensor_id, data)
    if leitura:
        return jsonify(leitura.to_dict()), 201
    return jsonify({"error": "Leitura não registrada"}), 400

@leituras_bp.get("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/leituras")
def listar(dispositivo_uuid, sensor_id):
    leituras = leitura_service.listar_leituras(dispositivo_uuid, sensor_id)
    return jsonify([l.to_dict() for l in leituras])

@leituras_bp.get("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/leituras/<int:leitura_id>")
def obter(dispositivo_uuid, sensor_id, leitura_id):
    leitura = leitura_service.obter_leitura_por_id(dispositivo_uuid, sensor_id, leitura_id)
    if leitura:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada"}), 404

@leituras_bp.patch("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/leituras/<int:leitura_id>")
def atualizar_status(dispositivo_uuid, sensor_id, leitura_id):
    data = request.json
    resolvido = data.get("resolvido")
    if resolvido is None:
        return jsonify({"error": "Campo 'resolvido' é obrigatório"}), 400

    leitura = leitura_service.atualizar_status_leitura(dispositivo_uuid, sensor_id, leitura_id, resolvido)
    if leitura:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada"}), 404

@leituras_bp.delete("/dispositivos/<dispositivo_uuid>/sensores/<int:sensor_id>/leituras/<int:leitura_id>")
def remover(dispositivo_uuid, sensor_id, leitura_id):
    sucesso = leitura_service.remover_leitura(dispositivo_uuid, sensor_id, leitura_id)
    if sucesso:
        return "", 204
    return jsonify({"error": "Leitura não encontrada"}), 404
