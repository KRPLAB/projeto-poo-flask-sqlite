from flask import Blueprint, jsonify, request
from services.leitura_service import registrar_leitura, listar_leituras_por_sensor, obter_leitura_por_id, remover_leitura

leituras_bp = Blueprint("leituras", __name__)

# Criar leitura vinculada ao sensor
@leituras_bp.post("/sensores/<int:sensor_id>/leituras")
def criar(sensor_id):
    data = request.json
    valor = data.get("valor")
    leitura = registrar_leitura(sensor_id, valor)
    if leitura:
        return jsonify(leitura.to_dict()), 201
    return jsonify({"error": "Sensor inválido ou inativo"}), 400

# Listar leituras de um sensor
@leituras_bp.get("/sensores/<int:sensor_id>/leituras")
def listar(sensor_id):
    leituras = listar_leituras_por_sensor(sensor_id)
    return jsonify([l.to_dict() for l in leituras])

# Obter leitura por id e sensor
@leituras_bp.get("/sensores/<int:sensor_id>/leituras/<int:leitura_id>")
def obter(sensor_id, leitura_id):
    leitura = obter_leitura_por_id(leitura_id)
    if leitura and leitura.sensor_id == sensor_id:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada para este sensor"}), 404

# Remover leitura por id e sensor
@leituras_bp.delete("/sensores/<int:sensor_id>/leituras/<int:leitura_id>")
def remover(sensor_id, leitura_id):
    sucesso = remover_leitura(leitura_id, sensor_id)
    if sucesso:
        return jsonify({"message": "Leitura removida com sucesso"})
    return jsonify({"error": "Leitura não encontrada para este sensor"}), 404

