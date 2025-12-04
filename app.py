import os
from flask import Flask
from flask_cors import CORS
from routes.dispositivo import dispositivos_bp
from routes.sensores import sensores_bp
from routes.leitura import leituras_bp
from routes.alertas import alertas_bp
from database.dispositivo_dao import DispositivoDAO
from database.sensor_dao import SensorDAO
from database.leitura_dao import LeituraDAO
from database.alerta_dao import AlertaDAO
import threading
import mqtt.client as mqtt_client

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(dispositivos_bp)
app.register_blueprint(sensores_bp)
app.register_blueprint(leituras_bp)
app.register_blueprint(alertas_bp)

def init_db():
    DispositivoDAO.criar_tabela()
    SensorDAO.criar_tabela()
    LeituraDAO.criar_tabela()
    AlertaDAO.criar_tabela()

def start_mqtt_client():
    mqtt_client.start()

if __name__ == "__main__":
    init_db()
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        mqtt_thread = threading.Thread(target=start_mqtt_client)
        mqtt_thread.start()
    app.run(debug=True)
