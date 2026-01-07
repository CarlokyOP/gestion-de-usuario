from app.database import db
from datetime import datetime


class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)

    # Información básica
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    # Fecha y hora (editable desde formulario)
    fecha_creacion = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    # Estado del ticket
    # Nuevo | Apertura | Resuelto | Cierre | Escalado
    estado = db.Column(
        db.String(20),
        nullable=False,
        default='Nuevo'
    )

    # Prioridad
    # Baja | Media | Alta
    prioridad = db.Column(
        db.String(10),
        nullable=False
    )

    # Cliente
    nombre_cliente = db.Column(db.String(100), nullable=False)
    telefono_cliente = db.Column(db.String(30), nullable=False)
    correo_cliente = db.Column(db.String(120), nullable=False)

    # Clasificación
    # Hardware | Movil | Red | Otro
    tipo_problema = db.Column(db.String(30), nullable=False)

    # Fuente del ticket (puede tener múltiples valores)
    # Se guarda como texto separado por comas
    fuente_ticket = db.Column(db.String(100), nullable=False)

    # ==============================
    # NUEVOS CAMPOS (SOPORTE TI)
    # ==============================

    # Medidas adoptadas por el técnico
    medidas_adoptadas = db.Column(db.Text, nullable=True)

    # Resolución del ticket
    resolucion = db.Column(db.Text, nullable=True)

    # Técnico(s) a cargo
    tecnico_a_cargo = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return f"<Ticket {self.id} - {self.titulo}>"
