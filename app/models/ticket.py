from app import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)

    # Información básica
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    # Fecha y hora
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Estado del ticket
    estado = db.Column(db.String(20), nullable=False, default='Nuevo')
    # Nuevo | Apertura | Resuelto | Cierre | Escalado

    # Prioridad
    prioridad = db.Column(db.String(10), nullable=False)
    # Baja | Media | Alta

    # Cliente
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(30), nullable=False)
    correo_cliente = db.Column(db.String(120), nullable=False)

    # Clasificación
    tipo_problema = db.Column(db.String(30), nullable=False)
    # Hardware | Movil | Red | Otro

    fuente_ticket = db.Column(db.String(30), nullable=False)
    # Llamada | Correo | WebChat | Presencial

    def __repr__(self):
        return f"<Ticket {self.id} - {self.titulo}>"



