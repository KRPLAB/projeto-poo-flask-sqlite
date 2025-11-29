from flask import Blueprint, jsonify, request
from services.dispositivo_service import criar_dispositivo, listar_dispositivos, obter_dispositivo_por_id, remover_dispositivo, atualizar_dispositivo

dispositivos_bp = Blueprint("dispositivos", __name__)

@dispositivos_bp.post("/dispositivos")
def criar():
    data = request.json
    dispositivo = criar_dispositivo(data["tipo"], data["localizacao"])
    return jsonify(dispositivo.to_dict()), 201

@dispositivos_bp.get("/dispositivos")
def listar():
    dispositivos = listar_dispositivos()
    return jsonify([d.to_dict() for d in dispositivos])

@dispositivos_bp.get("/dispositivos/<int:dispositivo_id>")
def obter(dispositivo_id):
    dispositivo = obter_dispositivo_por_id(dispositivo_id)
    if dispositivo:
        return jsonify(dispositivo.to_dict())
    return jsonify({"error": "Dispositivo não encontrado"}), 404

@dispositivos_bp.delete("/dispositivo/<int:dispositivo_id>/remove")
def remover(dispositivo_id):
    sucesso = remover_dispositivo(dispositivo_id)
    if sucesso:
        return jsonify({"message": "Dispositivo removido com sucesso"})
    return jsonify({"error": "Dispositivo não encontrado"}), 404

@dispositivos_bp.put("/dispositivo/<int:dispositivo_id>/update")
def atualizar(dispositivo_id):
    data = request.json
    dispositivo = atualizar_dispositivo(dispositivo_id, data["tipo"], data["localizacao"], data["ativo"])
    if dispositivo:
        return jsonify(dispositivo.to_dict())
    return jsonify({"error": "Dispositivo não encontrado"}), 404

