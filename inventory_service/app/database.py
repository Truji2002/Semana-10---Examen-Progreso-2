from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuración de Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:9060@localhost/inventory_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

# Modelo de la tabla 'rooms'
class Room(db.Model):
    __tablename__ = 'rooms'
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.Integer, nullable=False, unique=True)
    room_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_number": self.room_number,
            "room_type": self.room_type,
            "status": self.status
        }
