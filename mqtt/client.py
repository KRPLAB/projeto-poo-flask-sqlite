import json
import paho.mqtt.client as mqtt


from models.leitura import Leitura
from models.alarme import Alerta
from database.leitura_dao import LeituraDAO
from database.alarme_dao import AlarmeDAO
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_BASE = os.getenv("MQTT_TOPIC_BASE", "{id_dispositivo}/sensores")


def processa_leitura(data: dict):
    leitura = Leitura(
        id=None,
        sensor_id=data["sensor_id"],
        valor=float(data["valor"]),
        timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else None
    )
    LeituraDAO.salvar(leitura)
    print(f"Leitura salva: {leitura.to_dict()}")

    if leitura.e_alerta():
        print(f"Alerta! Leitura excedeu o limite: {leitura.valor}")

def processa_alerta(data: dict):
    alerta = Alerta(
        id=None,
        nivel_severidade=data["nivel_severidade"],
        mensagem=data["mensagem"],
        ativo=data.get("ativo", True)
    )
    AlarmeDAO.salvar(alerta)
    print(f"Alerta salvo: {alerta}")


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código de resultado {rc}")
    # Assina todos os tópicos no padrão id_dispositivo/sensores/leituras/id_sensor e id_dispositivo/sensores/alertas/id_sensor
    client.subscribe("+/sensores/leituras/+")
    client.subscribe("+/sensores/alertas/+")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Mensagem recebida no tópico {topic}: {payload}")

    # Espera-se o formato: id_dispositivo/sensores/leituras/id_sensor ou id_dispositivo/sensores/alertas/id_sensor
    try:
        data = json.loads(payload)
        partes = topic.split('/')
        if len(partes) == 4:
            id_dispositivo = partes[0]
            tipo = partes[2]
            id_sensor = partes[3]
            data["dispositivo_id"] = id_dispositivo
            data["sensor_id"] = int(id_sensor)
            if tipo == "leituras":
                processa_leitura(data)
            elif tipo == "alertas":
                processa_alerta(data)
            else:
                print(f"Tópico desconhecido: {topic}")
        else:
            print(f"Formato de tópico inválido: {topic}")
    except Exception as e:
        print(f"Erro ao processar a mensagem: {e}")

def start():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    start()