from flask import Blueprint, jsonify, request
from services.alerta_service import criar_alerta, listar_alertas_por_sensor, obter_alerta_por_id, remover_alerta

alertas_bp = Blueprint("alertas", __name__)

# Criar alerta vinculado ao sensor
@alertas_bp.post("/sensores/<int:sensor_id>/alertas")
def criar(sensor_id):
    data = request.json
    alerta = criar_alerta(sensor_id, data)
    if alerta:
        return jsonify(alerta.to_dict()), 201
    return jsonify({"error": "Sensor inválido ou alerta não criado"}), 400

# Listar alertas de um sensor
@alertas_bp.get("/sensores/<int:sensor_id>/alertas")
def listar(sensor_id):
    alertas = listar_alertas_por_sensor(sensor_id)
    return jsonify([a.to_dict() for a in alertas])

# Obter alerta por id e sensor
@alertas_bp.get("/sensores/<int:sensor_id>/alertas/<int:alerta_id>")
def obter(sensor_id, alerta_id):
    alerta = obter_alerta_por_id(alerta_id)
    if alerta and alerta.sensor_id == sensor_id:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado para este sensor"}), 404

# Remover alerta por id e sensor
@alertas_bp.delete("/sensores/<int:sensor_id>/alertas/<int:alerta_id>")
def remover(sensor_id, alerta_id):
    sucesso = remover_alerta(alerta_id, sensor_id)
    if sucesso:
        return jsonify({"message": "Alerta removido com sucesso"})
    return jsonify({"error": "Alerta não encontrado para este sensor"}), 404
