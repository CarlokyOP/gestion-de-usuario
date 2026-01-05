from app import db
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='Abierto')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    prioridad = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Ticket {self.id} - {self.titulo}>'
