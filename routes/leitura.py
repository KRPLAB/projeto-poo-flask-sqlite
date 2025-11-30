from flask import Blueprint, jsonify, request
from services.leitura_service import LeituraService

leituras_bp = Blueprint("leituras", __name__)
leitura_service = LeituraService()

@leituras_bp.post("/leituras")
def criar():
    data = request.json
    leitura = leitura_service.registrar_leitura(data)
    if leitura:
        return jsonify(leitura.to_dict()), 201
    return jsonify({"error": "Leitura não registrada"}), 400

@leituras_bp.get("/leituras")
def listar():
    leituras = leitura_service.listar_leituras()
    return jsonify([l.to_dict() for l in leituras])

@leituras_bp.get("/leituras/<int:leitura_id>")
def obter(leitura_id):
    leitura = leitura_service.obter_leitura_por_id(leitura_id)
    if leitura:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada"}), 404

@leituras_bp.put("/leituras/<int:leitura_id>")
def atualizar(leitura_id):
    data = request.json
    leitura = leitura_service.atualizar_leitura(leitura_id, data)
    if leitura:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada"}), 404
