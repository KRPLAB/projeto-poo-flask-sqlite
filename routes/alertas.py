from flask import Blueprint, jsonify, request
from services.alerta_service import AlertaService

alertas_bp = Blueprint("alertas", __name__)
alerta_service = AlertaService()

@alertas_bp.post("/alertas")
def criar():
    data = request.json
    alerta = alerta_service.criar_alerta(data)
    if alerta:
        return jsonify(alerta.to_dict()), 201
    return jsonify({"error": "Alerta não criado"}), 400

@alertas_bp.get("/alertas")
def listar():
    alertas = alerta_service.listar_alertas()
    return jsonify([a.to_dict() for a in alertas])

@alertas_bp.get("/alertas/<int:alerta_id>")
def obter(alerta_id):
    alerta = alerta_service.obter_alerta_por_id(alerta_id)
    if alerta:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado"}), 404

@alertas_bp.delete("/alertas/<int:alerta_id>")
def remover(alerta_id):
    sucesso = alerta_service.remover_alerta(alerta_id)
    if sucesso:
        return jsonify({"message": "Alerta removido com sucesso"})
    return jsonify({"error": "Alerta não encontrado"}), 404

@alertas_bp.put("/alertas/<int:alerta_id>")
def atualizar(alerta_id):
    data = request.json
    alerta = alerta_service.atualizar_alerta(alerta_id, data)
    if alerta:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado"}), 404
