from flask import Blueprint, jsonify, request
from services.dispositivo_service import DispositivoService

dispositivos_bp = Blueprint("dispositivos", __name__)
dispositivo_service = DispositivoService()

@dispositivos_bp.post("/dispositivos")
def criar():
    data = request.json
    dispositivo = dispositivo_service.criar_dispositivo(data)
    return jsonify(dispositivo.to_dict()), 201

@dispositivos_bp.get("/dispositivos")
def listar():
    dispositivos = dispositivo_service.listar_dispositivos()
    return jsonify([d.to_dict() for d in dispositivos])

@dispositivos_bp.get("/dispositivos/<uuid>")
def obter(uuid):
    dispositivo = dispositivo_service.obter_dispositivo_por_uuid(uuid)
    if dispositivo:
        return jsonify(dispositivo.to_dict())
    return jsonify({"error": "Dispositivo não encontrado"}), 404

@dispositivos_bp.delete("/dispositivos/<uuid>")
def remover(uuid):
    sucesso = dispositivo_service.remover_dispositivo(uuid)
    if sucesso:
        return jsonify({"message": "Dispositivo removido com sucesso"})
    return jsonify({"error": "Dispositivo não encontrado"}), 404

@dispositivos_bp.put("/dispositivos/<uuid>")
def atualizar(uuid):
    data = request.json
    dispositivo = dispositivo_service.atualizar_dispositivo(uuid, data)
    if dispositivo:
        return jsonify(dispositivo.to_dict())
    return jsonify({"error": "Dispositivo não encontrado"}), 404
