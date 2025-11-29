from flask import Flask
from routes.alertas import alertas_bp
import threading
import mqtt.client as mqtt_client

app = Flask(__name__)
app.register_blueprint(alertas_bp)

def start_mqtt_client():
    mqtt_client.start()

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.start()
    app.run(debug=True)
