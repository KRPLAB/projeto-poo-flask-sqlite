import json
import paho.mqtt.client as mqtt

from database.alerta_dao import AlertaDAO
from database.dispositivo_dao import DispositivoDAO
from models.leitura import Leitura
from models.alerta import Alerta
from models.dispositivo import Dispositivo
from database.leitura_dao import LeituraDAO
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_BASE = os.getenv("MQTT_TOPIC_BASE", "{id_dispositivo}/sensores")

# Referência global ao cliente para publicar mensagens
mqtt_client = None


def processa_registro(client, data: dict):
    """Processa registro de novos dispositivos"""
    try:
        mac_address = data.get("mac_address")
        if not mac_address:
            print("Erro: mac_address não fornecido no registro")
            return
        
        # Verifica se dispositivo já existe
        dispositivo = DispositivoDAO.obter_dispositivo_por_mac(mac_address)
        
        if not dispositivo:
            # Cria novo dispositivo
            dispositivo = Dispositivo(
                mac_address=mac_address,
                descricao=data.get("descricao"),
                status='online'
            )
            dispositivo = DispositivoDAO.salvar(dispositivo)
            print(f"Novo dispositivo registrado: {mac_address} -> {dispositivo.uuid}")
        else:
            # Atualiza status para online
            dispositivo.status = 'online'
            DispositivoDAO.update_dispositivo(dispositivo)
            print(f"Dispositivo existente conectado: {mac_address} -> {dispositivo.uuid}")
        
        # Publica resposta com UUID
        response_topic = f"dispositivos/registro/{mac_address}"
        response_payload = json.dumps({"uuid": dispositivo.uuid})
        client.publish(response_topic, response_payload)
        print(f"Resposta de registro enviada para {response_topic}")
        
    except Exception as e:
        print(f"Erro ao processar registro: {e}")


def processa_leitura(data: dict):
    """Processa leituras de sensores"""
    try:
        leitura = Leitura(
            id=None,
            sensor_id=data["sensor_id"],
            valor=float(data["valor"]),
            data_hora=datetime.fromisoformat(data["data_hora"]) if "data_hora" in data else None
        )
        LeituraDAO.salvar(leitura)
        print(f"====== Leitura registrada no banco de dados ======")
        print(f"Sensor ID: {leitura.sensor_id}, Valor: {leitura.valor}")
    except Exception as e:
        print(f"Erro ao processar leitura: {e}")

def processa_alerta(data: dict):
    """Processa alertas de sensores"""
    try:
        alerta = Alerta(
            id=None,
            sensor_id=data["sensor_id"],
            nivel=data["nivel"],
            mensagem=data.get("mensagem"),
            resolvido=False
        )
        AlertaDAO.salvar(alerta)
        print(f"====== Alerta registrado no banco de dados ======")
        print(f"Sensor ID: {alerta.sensor_id}, Nível: {alerta.nivel}")
    except Exception as e:
        print(f"Erro ao processar alerta: {e}")


def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código de resultado {rc}")
    # Assina tópicos de leituras, alertas e registro
    client.subscribe("+/sensores/leituras/+")
    client.subscribe("+/sensores/alertas/+")
    client.subscribe("dispositivos/registro")
    print("Inscrito nos tópicos: +/sensores/leituras/+, +/sensores/alertas/+, dispositivos/registro")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Mensagem recebida no tópico {topic}: {payload}")

    try:
        data = json.loads(payload)
        
        # Verifica se é registro de dispositivo
        if topic == "dispositivos/registro":
            processa_registro(client, data)
            return
        
        # Processa leituras e alertas
        partes = topic.split('/')
        if len(partes) == 4:
            id_dispositivo = partes[0]
            tipo = partes[2]
            id_sensor = partes[3]
            
            # Extrai sensor_id do payload ou do tópico
            sensor_id = data.get("sensor", int(id_sensor))
            data["sensor_id"] = sensor_id
            data["dispositivo_id"] = id_dispositivo
            
            if tipo == "leituras" and "valor" in data:
                processa_leitura(data)
            elif tipo == "alertas" and "nivel" in data and "mensagem" in data:
                processa_alerta(data)
            else:
                print("===== Payload ou tópico inválido recebido =====")
        else:
            print(f"Formato de tópico inválido: {topic}")
            
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"===== Erro ao processar a mensagem recebida: =====", e)

def start():
    global mqtt_client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    print(f"Tentando conectar ao broker MQTT em {MQTT_BROKER}:{MQTT_PORT}")
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

if __name__ == "__main__":
    start()