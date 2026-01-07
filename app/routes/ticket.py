from flask import Blueprint, render_template, request, redirect, url_for
from app.database import db
from app.models.ticket import Ticket
from datetime import datetime

ticket_bp = Blueprint("ticket_bp", __name__, url_prefix="/tickets")


# ======================
# LISTAR TICKETS
# ======================
@ticket_bp.route("/")
def list_tickets():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template("ticket.html", tickets=tickets)


# ======================
# CREAR TICKET
# ======================
@ticket_bp.route("/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")

        fecha_hora = datetime.strptime(
            f"{fecha} {hora}", "%Y-%m-%d %H:%M"
        ) if fecha and hora else datetime.utcnow()

        ticket = Ticket(
            titulo=request.form["titulo"],
            descripcion=request.form["descripcion"],
            estado=request.form["estado"],
            prioridad=request.form["prioridad"],
            nombre_cliente=request.form["nombre_cliente"],
            telefono_cliente=request.form["telefono_cliente"],
            correo_cliente=request.form["correo_cliente"],
            tipo_problema=request.form["tipo_problema"],
            fuente_ticket=request.form["fuente_ticket"],
            fecha_creacion=fecha_hora
        )

        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("ticket_bp.list_tickets"))

    return render_template("ticket_form.html", ticket=None)


# ======================
# EDITAR TICKET
# ======================
@ticket_bp.route("/<int:ticket_id>/edit", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if request.method == "POST":
        ticket.titulo = request.form["titulo"]
        ticket.descripcion = request.form["descripcion"]
        ticket.estado = request.form["estado"]
        ticket.prioridad = request.form["prioridad"]
        ticket.nombre_cliente = request.form["nombre_cliente"]
        ticket.telefono_cliente = request.form["telefono_cliente"]
        ticket.correo_cliente = request.form["correo_cliente"]
        ticket.tipo_problema = request.form["tipo_problema"]
        ticket.fuente_ticket = request.form["fuente_ticket"]

        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        if fecha and hora:
            ticket.fecha_creacion = datetime.strptime(
                f"{fecha} {hora}", "%Y-%m-%d %H:%M"
            )

        db.session.commit()
        return redirect(url_for("ticket_bp.list_tickets"))

    return render_template("ticket_form.html", ticket=ticket)
