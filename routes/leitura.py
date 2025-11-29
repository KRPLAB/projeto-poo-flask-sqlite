from flask import Blueprint, jsonify, request
from services.leitura_service import registrar_leitura, listar_leituras, obter_leitura_por_id

leituras_bp = Blueprint("leituras", __name__)

@leituras_bp.post("/leituras")
def criar():
    data = request.json
    leitura = registrar_leitura(data["dispositivo_id"], data["valor"], data["timestamp"])
    return jsonify(leitura.to_dict()), 201

@leituras_bp.get("/leituras")
def listar():
    leituras = listar_leituras()
    return jsonify([l.to_dict() for l in leituras])

@leituras_bp.get("/leituras/<int:leitura_id>")
def obter(leitura_id):
    leitura = obter_leitura_por_id(leitura_id)
    if leitura:
        return jsonify(leitura.to_dict())
    return jsonify({"error": "Leitura não encontrada"}), 404

