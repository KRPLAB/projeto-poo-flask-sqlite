import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_device_creation():
    """Testa a criação de um novo dispositivo."""
    print("--- Testando criação de Dispositivo ---")
    url = f"{BASE_URL}/dispositivos"
    payload = {
        "mac_address": "00:1B:44:11:3A:B7",
        "descricao": "Dispositivo da Sala de Servidores"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP
        device_data = response.json()
        print("Dispositivo criado com sucesso:")
        print(json.dumps(device_data, indent=2))
        return device_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar dispositivo: {e}")
        return None

def test_sensor_creation(device_uuid):
    """Testa a criação de um sensor associado a um dispositivo."""
    if not device_uuid:
        return None
    
    print("\n--- Testando criação de Sensor ---")
    url = f"{BASE_URL}/sensores"
    payload = {
        "tipo": "Temperatura",
        "localizacao": "Rack 3, Posição 5",
        "dispositivo_uuid": device_uuid
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        sensor_data = response.json()
        print("Sensor criado com sucesso:")
        print(json.dumps(sensor_data, indent=2))
        return sensor_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar sensor: {e}")
        return None

def test_reading_registration(sensor_id):
    """Testa o registro de uma leitura para um sensor."""
    if not sensor_id:
        return None

    print("\n--- Testando registro de Leitura ---")
    url = f"{BASE_URL}/leituras"
    payload = {
        "sensor_id": sensor_id,
        "valor": 45.5
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        reading_data = response.json()
        print("Leitura registrada com sucesso:")
        print(json.dumps(reading_data, indent=2))
        return reading_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao registrar leitura: {e}")
        return None

def test_alert_creation(sensor_id):
    """Testa a criação de um alerta para um sensor."""
    if not sensor_id:
        return None

    print("\n--- Testando criação de Alerta ---")
    url = f"{BASE_URL}/alertas"
    payload = {
        "sensor_id": sensor_id,
        "nivel": "alto",
        "mensagem": "Temperatura excedeu o limite crítico!"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        alert_data = response.json()
        print("Alerta criado com sucesso:")
        print(json.dumps(alert_data, indent=2))
        return alert_data
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar alerta: {e}")
        return None

if __name__ == "__main__":
    # 1. Criar Dispositivo
    device = test_device_creation()
    
    if device:
        # 2. Criar Sensor
        sensor = test_sensor_creation(device.get("uuid"))
        
        if sensor:
            # 3. Registrar Leitura
            test_reading_registration(sensor.get("id"))
            
            # 4. Criar Alerta
            test_alert_creation(sensor.get("id"))
