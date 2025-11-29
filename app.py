from flask import Flask
from routes.alertas import alertas_bp

app = Flask(__name__)
app.register_blueprint(alertas_bp)

if __name__ == "__main__":
    app.run(debug=True)
