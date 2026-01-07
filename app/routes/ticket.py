from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from app.database import db
from app.models.ticket import Ticket

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


# =========================
# LISTADO
# =========================
@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


# =========================
# CREAR
# =========================
@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":

        # Fecha
        fecha_creacion = datetime.utcnow()

        # Fuente (checkbox múltiple)
        fuentes = request.form.getlist("fuente_ticket")
        fuente_ticket = ", ".join(fuentes)

        # Tipo de problema (checkbox múltiple)
        tipos = request.form.getlist("tipo_problema")
        tipo_problema = ", ".join(tipos)

        ticket = Ticket(
            titulo=request.form.get("titulo"),
            descripcion=request.form.get("descripcion"),
            fecha_creacion=fecha_creacion,
            estado=request.form.get("estado"),
            prioridad=request.form.get("prioridad"),
            nombre_cliente=request.form.get("nombre_cliente"),
            telefono_cliente=request.form.get("telefono_cliente"),
            correo_cliente=request.form.get("correo_cliente"),
            tipo_problema=tipo_problema,
            fuente_ticket=fuente_ticket,

            # Campos nuevos (opcionales)
            medidas_adoptadas=request.form.get("medidas_adoptadas"),
            resolucion=request.form.get("resolucion"),
            tecnico_a_cargo=request.form.get("tecnico_a_cargo"),
        )

        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=None)


# =========================
# DETALLE
# =========================
@ticket_bp.route("/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("ticket_detail.html", ticket=ticket)


# =========================
# EDITAR
# =========================
@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":
        ticket.titulo = request.form.get("titulo")
        ticket.descripcion = request.form.get("descripcion")
        ticket.estado = request.form.get("estado")
        ticket.prioridad = request.form.get("prioridad")
        ticket.nombre_cliente = request.form.get("nombre_cliente")
        ticket.telefono_cliente = request.form.get("telefono_cliente")
        ticket.correo_cliente = request.form.get("correo_cliente")

        ticket.fuente_ticket = ", ".join(request.form.getlist("fuente_ticket"))
        ticket.tipo_problema = ", ".join(request.form.getlist("tipo_problema"))

        ticket.medidas_adoptadas = request.form.get("medidas_adoptadas")
        ticket.resolucion = request.form.get("resolucion")
        ticket.tecnico_a_cargo = request.form.get("tecnico_a_cargo")

        db.session.commit()
        return redirect(url_for("ticket.ticket_detail", ticket_id=ticket.id))

    return render_template("ticket_form.html", ticket=ticket)


# =========================
# ELIMINAR
# =========================
@ticket_bp.route("/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("ticket.list_tickets"))
