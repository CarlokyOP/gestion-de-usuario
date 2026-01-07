from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from app.database import db
from app.models.ticket import Ticket

ticket_bp = Blueprint("ticket", __name__, url_prefix="/tickets")


# =========================
# LISTADO DE TICKETS
# =========================
@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


# =========================
# CREAR TICKET
# =========================
@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        # Fecha y hora editable
        fecha_str = request.form.get("fecha")
        hora_str = request.form.get("hora")

        if fecha_str and hora_str:
            fecha_creacion = datetime.strptime(
                f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M"
            )
        else:
            fecha_creacion = datetime.utcnow()

        # Fuente del ticket (checkbox múltiple)
        fuentes = request.form.getlist("fuente_ticket")
        fuente_ticket = ", ".join(fuentes)

        ticket = Ticket(
            titulo=request.form["titulo"],
            descripcion=request.form["descripcion"],
            fecha_creacion=fecha_creacion,
            estado=request.form["estado"],
            prioridad=request.form["prioridad"],
            nombre_cliente=request.form["nombre_cliente"],
            telefono_cliente=request.form["telefono_cliente"],
            correo_cliente=request.form["correo_cliente"],
            tipo_problema=request.form["tipo_problema"],
            fuente_ticket=fuente_ticket,

            # Nuevos campos
            medidas_adoptadas=request.form.get("medidas_adoptadas"),
            resolucion=request.form.get("resolucion"),
            tecnico_a_cargo=request.form.get("tecnico_a_cargo"),
        )

        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("ticket.list_tickets"))

    return render_template("ticket_form.html", ticket=None)


# =========================
# DETALLE DEL TICKET
# =========================
@ticket_bp.route("/<int:ticket_id>")
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    return render_template("ticket_detail.html", ticket=ticket)


# =========================
# EDITAR TICKET
# =========================
@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":
        fecha_str = request.form.get("fecha")
        hora_str = request.form.get("hora")

        if fecha_str and hora_str:
            ticket.fecha_creacion = datetime.strptime(
                f"{fecha_str} {hora_str}", "%Y-%m-%d %H:%M"
            )

        ticket.titulo = request.form["titulo"]
        ticket.descripcion = request.form["descripcion"]
        ticket.estado = request.form["estado"]
        ticket.prioridad = request.form["prioridad"]
        ticket.nombre_cliente = request.form["nombre_cliente"]
        ticket.telefono_cliente = request.form["telefono_cliente"]
        ticket.correo_cliente = request.form["correo_cliente"]
        ticket.tipo_problema = request.form["tipo_problema"]

        fuentes = request.form.getlist("fuente_ticket")
        ticket.fuente_ticket = ", ".join(fuentes)

        # Nuevos campos
        ticket.medidas_adoptadas = request.form.get("medidas_adoptadas")
        ticket.resolucion = request.form.get("resolucion")
        ticket.tecnico_a_cargo = request.form.get("tecnico_a_cargo")

        db.session.commit()
        return redirect(url_for("ticket.ticket_detail", ticket_id=ticket.id))

    return render_template("ticket_form.html", ticket=ticket)


# =========================
# ELIMINAR TICKET
# =========================
@ticket_bp.route("/<int:ticket_id>/delete", methods=["POST"])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for("ticket.list_tickets"))
