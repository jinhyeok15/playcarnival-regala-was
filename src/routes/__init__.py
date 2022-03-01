from flask import Flask
import record

app = Flask(__name__)
app.register_blueprint(record.bp)
