from flask import Flask
from routes import record

app = Flask("app")
app.register_blueprint(record.bp)
