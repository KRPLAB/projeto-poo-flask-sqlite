from flask import Blueprint, jsonify, request
from services.alerta_service import criar_alerta, listar_alertas, obter_alerta_por_id, remover_alerta

alertas_bp = Blueprint("alertas", __name__)

@alertas_bp.post("/alertas")
def criar():
    data = request.json
    alerta = criar_alerta(data)
    return jsonify(alerta.to_dict()), 201

@alertas_bp.get("/alertas")
def listar():
    alertas = listar_alertas()
    return jsonify([a.to_dict() for a in alertas])

@alertas_bp.get("/alertas/<int:alerta_id>")
def obter(alerta_id):
    alerta = obter_alerta_por_id(alerta_id)
    if alerta:
        return jsonify(alerta.to_dict())
    return jsonify({"error": "Alerta não encontrado"}), 404

@alertas_bp.delete("/alerta/<int:alerta_id>/remove")
def remover(alerta_id):
    sucesso = remover_alerta(alerta_id)
    if sucesso:
        return jsonify({"message": "Alerta removido com sucesso"})
    return jsonify({"error": "Alerta não encontrado"}), 404
